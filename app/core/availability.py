from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from motor.motor_asyncio import AsyncIOMotorDatabase

WEEKDAY_NAMES = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday",
]


def _parse_hhmm(s: str) -> time:
    h, m = s.split(":")
    return time(int(h), int(m))


def windows_for_day(working_hours: list[dict], day_name: str) -> list[tuple[time, time]]:
    entry = next((w for w in working_hours if w["day"] == day_name), None)
    if not entry or entry.get("closed"):
        return []
    open_t = _parse_hhmm(entry["open"])
    close_t = _parse_hhmm(entry["close"])
    if open_t >= close_t:
        return []

    windows: list[tuple[time, time]] = [(open_t, close_t)]
    for br in entry.get("breaks") or []:
        b_start = _parse_hhmm(br["start"])
        b_end = _parse_hhmm(br["end"])
        new_windows: list[tuple[time, time]] = []
        for w_start, w_end in windows:
            if b_end <= w_start or b_start >= w_end:
                new_windows.append((w_start, w_end))
                continue
            if b_start > w_start:
                new_windows.append((w_start, b_start))
            if b_end < w_end:
                new_windows.append((b_end, w_end))
        windows = new_windows
    return windows


def _intersect(
    a: list[tuple[time, time]], b: list[tuple[time, time]]
) -> list[tuple[time, time]]:
    out: list[tuple[time, time]] = []
    for a_start, a_end in a:
        for b_start, b_end in b:
            s = max(a_start, b_start)
            e = min(a_end, b_end)
            if s < e:
                out.append((s, e))
    return out


def is_special_closure(business: dict, target_date: date) -> dict | None:
    iso = target_date.isoformat()
    for sd in business.get("special_days") or []:
        sd_date = sd["date"]
        if isinstance(sd_date, datetime):
            sd_date = sd_date.date().isoformat()
        elif isinstance(sd_date, date):
            sd_date = sd_date.isoformat()
        if sd_date == iso:
            return sd
    return None


def is_in_time_off(staff: dict, target_date: date) -> bool:
    for off in staff.get("time_off") or []:
        s = off["start_date"]
        e = off["end_date"]
        if isinstance(s, str):
            s = date.fromisoformat(s)
        if isinstance(e, str):
            e = date.fromisoformat(e)
        if s <= target_date <= e:
            return True
    return False


def _ranges_overlap(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    return a_start < b_end and b_start < a_end


async def compute_available_slots(
    db: AsyncIOMotorDatabase,
    business: dict,
    service: dict,
    staff: dict,
    target_date: date,
    step_minutes: int = 15,
    now_utc: datetime | None = None,
) -> list[datetime]:
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)

    tz = ZoneInfo(business.get("timezone", "Europe/Istanbul"))
    duration = int(service["duration_minutes"])
    buf_before = int(service.get("buffer_before_minutes", 0))
    buf_after = int(service.get("buffer_after_minutes", 0))

    booking_buffer = int(
        (business.get("ai_settings") or {}).get("booking_buffer_minutes", 30)
    )

    closure = is_special_closure(business, target_date)
    if closure and closure.get("closed"):
        return []

    biz_wh = business["working_hours"]
    if closure and not closure.get("closed") and closure.get("open") and closure.get("close"):
        biz_windows = [(_parse_hhmm(closure["open"]), _parse_hhmm(closure["close"]))]
    else:
        biz_windows = windows_for_day(biz_wh, WEEKDAY_NAMES[target_date.weekday()])

    if not biz_windows:
        return []

    if is_in_time_off(staff, target_date):
        return []

    staff_wh = staff.get("working_hours") or biz_wh
    staff_windows = windows_for_day(staff_wh, WEEKDAY_NAMES[target_date.weekday()])
    if not staff_windows:
        return []

    windows = _intersect(biz_windows, staff_windows)
    if not windows:
        return []

    day_start_local = datetime.combine(target_date, time(0, 0), tzinfo=tz)
    day_end_local = day_start_local + timedelta(days=1)
    day_start_utc = day_start_local.astimezone(timezone.utc)
    day_end_utc = day_end_local.astimezone(timezone.utc)

    cursor = db.appointments.find({
        "business_id": business["_id"],
        "staff_id": staff["_id"],
        "status": {"$in": ["pending", "confirmed"]},
        "start_time": {"$lt": day_end_utc},
        "end_time": {"$gt": day_start_utc},
    }, {"start_time": 1, "end_time": 1, "room_id": 1})
    busy: list[tuple[datetime, datetime, str | None]] = []
    async for a in cursor:
        busy.append((a["start_time"], a["end_time"], a.get("room_id")))

    rooms = business.get("rooms") or []
    requires_room = bool(service.get("requires_room"))
    room_count = len(rooms)
    room_busy: list[tuple[datetime, datetime]] = []
    if requires_room and room_count > 0:
        cursor = db.appointments.find({
            "business_id": business["_id"],
            "status": {"$in": ["pending", "confirmed"]},
            "room_id": {"$ne": None},
            "start_time": {"$lt": day_end_utc},
            "end_time": {"$gt": day_start_utc},
        }, {"start_time": 1, "end_time": 1})
        async for a in cursor:
            room_busy.append((a["start_time"], a["end_time"]))

    earliest_allowed = now_utc + timedelta(minutes=booking_buffer)
    candidates: list[datetime] = []

    for w_start, w_end in windows:
        cur_local = datetime.combine(target_date, w_start, tzinfo=tz)
        win_end_local = datetime.combine(target_date, w_end, tzinfo=tz)
        # adımı step_minutes'a hizala (sürede %step_minutes != 0 olabilir)
        while cur_local + timedelta(minutes=duration) <= win_end_local:
            start_utc = cur_local.astimezone(timezone.utc)
            end_utc = start_utc + timedelta(minutes=duration)
            blocked_start = start_utc - timedelta(minutes=buf_before)
            blocked_end = end_utc + timedelta(minutes=buf_after)

            if start_utc < earliest_allowed:
                cur_local += timedelta(minutes=step_minutes)
                continue

            conflict = any(
                _ranges_overlap(blocked_start, blocked_end, b_s, b_e)
                for (b_s, b_e, _r) in busy
            )
            if conflict:
                cur_local += timedelta(minutes=step_minutes)
                continue

            if requires_room and room_count > 0:
                concurrent = sum(
                    1 for (b_s, b_e) in room_busy
                    if _ranges_overlap(blocked_start, blocked_end, b_s, b_e)
                )
                if concurrent >= room_count:
                    cur_local += timedelta(minutes=step_minutes)
                    continue

            candidates.append(start_utc)
            cur_local += timedelta(minutes=step_minutes)

    return candidates


async def find_first_available_slots(
    db: AsyncIOMotorDatabase,
    business: dict,
    service: dict,
    staff: dict,
    start_date: date,
    days_to_scan: int = 14,
    max_slots: int = 6,
    step_minutes: int = 15,
    now_utc: datetime | None = None,
) -> list[datetime]:
    out: list[datetime] = []
    for i in range(days_to_scan):
        d = start_date + timedelta(days=i)
        slots = await compute_available_slots(
            db, business, service, staff, d, step_minutes=step_minutes, now_utc=now_utc
        )
        for s in slots:
            out.append(s)
            if len(out) >= max_slots:
                return out
    return out
