from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

from app.voice.dialog import (
    DialogManager,
    Pending,
    _repair_date_stt,
    _date_spoken,
    _format_slot_ranges,
    _no_more_requests,
    _slot_ranges,
    _time_from_text,
    _yes,
)


class VoiceDialogStaffTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.dialog = DialogManager(
            {"name": "Randevum Online", "_id": "business"}, "+905000000000", "call"
        )
        self.dialog.staff = [
            {"_id": "m", "name": "Mehmet Kaya", "service_ids": ["s"]},
            {"_id": "y", "name": "Yusuf Demir", "service_ids": ["s"]},
            {"_id": "a", "name": "Ahmet Yılmaz", "service_ids": ["s"]},
            {"_id": "e", "name": "Emre Şahin", "service_ids": ["s"]},
        ]
        self.dialog.services = [{"_id": "s", "name": "Saç Kesimi"}]
        self.interpret_patch = patch.object(
            DialogManager, "_interpret", AsyncMock(return_value={})
        )
        self.interpret_patch.start()
        self.slot_status_patch = patch.object(
            DialogManager,
            "_requested_slot_status",
            AsyncMock(return_value="available"),
        )
        self.slot_status_patch.start()

    def tearDown(self) -> None:
        self.slot_status_patch.stop()
        self.interpret_patch.stop()

    def test_matches_staff_by_first_name_only(self) -> None:
        self.assertEqual(self.dialog._match("Mehmet", self.dialog.staff)["_id"], "m")
        self.assertEqual(
            self.dialog._match("Emre'den randevu istiyorum", self.dialog.staff)["_id"],
            "e",
        )

    def test_accepts_common_stt_variant_of_yes(self) -> None:
        self.assertTrue(_yes("Evert"))

    def test_understands_spaced_hour_suffix_and_bare_hour(self) -> None:
        self.assertEqual(_time_from_text("Hayır, saat bir de olsun."), "13:00")
        self.assertEqual(_time_from_text("Bir.", allow_bare=True), "13:00")
        self.assertEqual(
            _time_from_text("Mehmet Bey'den yarına saat beşe alacağım"),
            "17:00",
        )
        self.assertEqual(_time_from_text("Yarın saat beş e olsun"), "17:00")
        self.assertEqual(_time_from_text("Saç, bir de.", allow_bare=True), "13:00")
        self.assertEqual(_time_from_text("Saç onişin.", allow_bare=True), "10:00")
        self.assertIsNone(_time_from_text("Bir randevu istiyorum"))

    def test_stt_prompt_only_contains_terms_expected_in_current_turn(self) -> None:
        state, prompt = self.dialog.stt_context()
        self.assertEqual(state, "staff")
        self.assertIn("Mehmet Kaya", prompt)
        self.assertNotIn("Saç Kesimi", prompt)

        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date(2026, 7, 21)
        state, prompt = self.dialog.stt_context()
        self.assertEqual(state, "time")
        self.assertIn("saat on iki", prompt)
        self.assertNotIn("Saç Kesimi", prompt)

    def test_repairs_phone_variants_without_changing_real_half_hour(self) -> None:
        self.assertEqual(
            _repair_date_stt("Yerin.", booking_context=True), "yarın."
        )
        self.assertEqual(
            _repair_date_stt("Yerim.", booking_context=True), "yarın."
        )
        self.assertEqual(
            _repair_date_stt("Yard.", booking_context=True), "yarın."
        )
        self.assertEqual(
            _repair_date_stt("Yerim.", booking_context=True), "yarın."
        )
        self.assertEqual(
            _repair_date_stt(
                "Mehmet Beyden yarım saat beşe saç kesimi alacağım",
                booking_context=True,
            ),
            "Mehmet Beyden yarın saat beşe saç kesimi alacağım",
        )
        self.assertEqual(
            _repair_date_stt("Yarım saat sonra.", booking_context=True),
            "Yarım saat sonra.",
        )

    def test_normalizes_stt_text_using_current_dialog_state(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.assertEqual(self.dialog.normalize_stt_text("Yerin."), "yarın.")

        self.dialog.target_date = date(2026, 7, 21)
        self.assertEqual(
            self.dialog.normalize_stt_text("Saç, bir de."), "saat bir de."
        )
        self.assertEqual(
            self.dialog.normalize_stt_text("Akşam deşe."), "Akşam beşe."
        )

    async def test_staff_question_uses_barber_word_and_first_names(self) -> None:
        answer = await self.dialog.respond("Randevu almak istiyorum")
        self.assertEqual(answer, "Tabii, hangi berberi tercih edersiniz?")

    async def test_first_name_advances_booking_without_llm(self) -> None:
        answer = await self.dialog.respond("Emre")
        self.assertEqual(self.dialog.staff_member["name"], "Emre Şahin")
        self.assertEqual(answer, "Peki, hangi işlemi yaptırmak istersiniz?")

    async def test_rejected_confirmation_applies_time_in_same_sentence(self) -> None:
        self.dialog.staff_member = self.dialog.staff[-1]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date(2026, 7, 28)
        self.dialog.target_time = "09:00"
        self.dialog.pending = Pending("create")

        answer = await self.dialog.respond("Hayır, saat bir de olsun.")

        self.assertEqual(self.dialog.target_time, "13:00")
        self.assertEqual(self.dialog.pending.action, "create")
        self.assertEqual(
            answer,
            "28 Temmuz saat 13:00, Emre Şahin, Saç Kesimi için "
            "randevuyu onaylıyor musunuz?",
        )

    async def test_combined_barber_time_and_date_keeps_every_entity(self) -> None:
        answer = await self.dialog.respond(
            "Mehmet Bey'den saat beşe alacağım yarın."
        )

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.target_date, date.today() + timedelta(days=1))
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertIsNone(self.dialog.service)
        self.assertEqual(answer, "Peki, hangi işlemi yaptırmak istersiniz?")

    async def test_complete_mixed_order_sentence_goes_to_confirmation(self) -> None:
        answer = await self.dialog.respond(
            "Saat 5'e Mehmet Bey'den yarın saç kesimi alacağım."
        )

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        tomorrow = date.today() + timedelta(days=1)
        self.assertEqual(self.dialog.target_date, tomorrow)
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertEqual(self.dialog.pending.action, "create")
        self.assertEqual(
            answer,
            f"{_date_spoken(tomorrow)} saat 17:00, Mehmet Kaya, Saç Kesimi için "
            "randevuyu onaylıyor musunuz?",
        )

    async def test_common_phone_stt_variant_yarim_is_repaired_in_booking(self) -> None:
        answer = await self.dialog.respond(
            "Mehmet Beyden saat beşe alacağım, yarım."
        )

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.target_date, date.today() + timedelta(days=1))
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertEqual(answer, "Peki, hangi işlemi yaptırmak istersiniz?")

    def test_understands_natural_appointment_information_request(self) -> None:
        self.assertEqual(
            self.dialog._local_intent("Az önce oluşturduğum randevunun bilgilerini söyle"),
            "list",
        )

    async def test_confirmation_accepts_repeated_entity_without_yes_no_loop(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog.target_time = "17:00"
        self.dialog.pending = Pending("create")

        answer = await self.dialog.respond(
            "Söyledim ya, Mehmet'ten saç kesimi istiyorum."
        )

        self.assertTrue(answer.startswith("Haklısınız"))
        self.assertIn("onaylıyor musunuz", answer)

    def test_llm_history_drops_old_conflicting_turns(self) -> None:
        self.dialog.history = [
            {"role": "user", "content": "Mehmet"},
            {"role": "assistant", "content": "Hangi işlem?"},
            {"role": "user", "content": "Saç kesimi"},
            {"role": "assistant", "content": "Hangi gün?"},
            {"role": "user", "content": "Hayır, sakal tıraşı"},
        ]
        self.assertEqual(
            self.dialog._llm_recent_history(),
            [
                {"role": "assistant", "content": "Hangi gün?"},
                {"role": "user", "content": "Hayır, sakal tıraşı"},
            ],
        )

    async def test_successful_booking_closes_dialog_after_farewell(self) -> None:
        self.dialog.customer = {"_id": "customer"}
        self.dialog.conversation = {"_id": "conversation"}
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog.target_time = "17:00"
        self.dialog.pending = Pending("create")

        with patch(
            "app.voice.dialog.create_appointment",
            AsyncMock(return_value={"appointment_id": "appointment"}),
        ):
            answer = await self.dialog._commit_create()

        self.assertFalse(self.dialog.closed)
        self.assertEqual(self.dialog.pending.action, "post_booking")
        self.assertIn("randevunuzu oluşturdum", answer)
        self.assertTrue(answer.endswith("Başka bir isteğiniz var mı?"))

        self.dialog.conversation = None
        closing = await self.dialog.respond("Hayır, yok.")
        self.assertTrue(self.dialog.closed)
        self.assertIsNone(self.dialog.pending)
        self.assertTrue(closing.endswith("İyi günler."))

    def test_post_booking_negative_must_be_short_and_unambiguous(self) -> None:
        self.assertTrue(_no_more_requests("Hayır, yok."))
        self.assertTrue(_no_more_requests("Başka bir isteğim yok"))
        self.assertFalse(
            _no_more_requests("Hayır yok ama arkadaşımın bilgilerini vereceğim")
        )

    async def test_full_time_is_rejected_before_confirmation(self) -> None:
        self.dialog._requested_slot_status.return_value = "time_full"

        answer = await self.dialog.respond(
            "Yarın saat beşe Mehmet Bey'den saç kesimi istiyorum."
        )

        self.assertIsNone(self.dialog.pending)
        self.assertIsNone(self.dialog.target_time)
        self.assertIsNotNone(self.dialog.target_date)
        self.assertIn("saat 17:00", answer)
        self.assertIn("dolu", answer)
        self.assertIn("Başka bir saat", answer)
        self.assertNotIn("onaylıyor musunuz", answer)

    async def test_full_date_is_rejected_before_confirmation(self) -> None:
        self.dialog._requested_slot_status.return_value = "date_full"

        answer = await self.dialog.respond(
            "Yarın saat beşe Mehmet Bey'den saç kesimi istiyorum."
        )

        self.assertIsNone(self.dialog.pending)
        self.assertIsNone(self.dialog.target_date)
        self.assertIsNone(self.dialog.target_time)
        self.assertIn("uygun saat kalmamış", answer)
        self.assertIn("Başka bir tarih", answer)
        self.assertNotIn("onaylıyor musunuz", answer)

    def test_contiguous_slots_are_spoken_as_one_range(self) -> None:
        tz = ZoneInfo("Europe/Istanbul")
        slots = [
            datetime(2026, 7, 22, hour, minute, tzinfo=tz).astimezone(timezone.utc)
            for hour, minute in (
                (9, 0), (9, 15), (9, 30), (9, 45), (10, 0), (10, 15),
                (10, 30), (10, 45), (11, 0), (11, 15), (11, 30),
            )
        ]

        ranges = _slot_ranges(slots, tz, duration_minutes=30)

        self.assertEqual(len(ranges), 1)
        self.assertEqual(_format_slot_ranges(ranges), "9 ile 12 arası")
