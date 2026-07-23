from __future__ import annotations

import unittest
from datetime import date

from app.voice.llm import parse_target_date_tr


class TurkishVoiceDateParserTests(unittest.TestCase):
    def test_next_week_wednesday_from_monday(self) -> None:
        value, label = parse_target_date_tr(
            "Haftaya çarşamba gününe randevu istiyorum",
            reference_date=date(2026, 7, 20),
        )
        self.assertEqual(value, date(2026, 7, 29))
        self.assertEqual(label, "Haftaya Çarşamba")

    def test_next_week_wednesday_from_saturday(self) -> None:
        value, _ = parse_target_date_tr(
            "Gelecek hafta çarşamba",
            reference_date=date(2026, 7, 25),
        )
        self.assertEqual(value, date(2026, 7, 29))

    def test_two_weeks_later_friday_uses_calendar_week(self) -> None:
        value, _ = parse_target_date_tr(
            "İki hafta sonra cuma",
            reference_date=date(2026, 7, 25),
        )
        self.assertEqual(value, date(2026, 8, 7))

    def test_same_weekday_without_modifier_means_next_occurrence(self) -> None:
        value, _ = parse_target_date_tr(
            "Çarşamba günü",
            reference_date=date(2026, 7, 22),
        )
        self.assertEqual(value, date(2026, 7, 29))

    def test_next_week_today_is_seven_days_later(self) -> None:
        value, label = parse_target_date_tr(
            "Haftaya bugün gelebilirim",
            reference_date=date(2026, 7, 23),
        )
        self.assertEqual(value, date(2026, 7, 30))
        self.assertEqual(label, "Haftaya bugün")

    def test_numeric_days_later(self) -> None:
        value, label = parse_target_date_tr(
            "3 gün sonra",
            reference_date=date(2026, 7, 23),
        )
        self.assertEqual(value, date(2026, 7, 26))
        self.assertEqual(label, "3 gün sonra")

    def test_spoken_days_later(self) -> None:
        value, _ = parse_target_date_tr(
            "Üç gün sonra için",
            reference_date=date(2026, 7, 23),
        )
        self.assertEqual(value, date(2026, 7, 26))

    def test_previous_relative_days_are_understood(self) -> None:
        yesterday, _ = parse_target_date_tr(
            "Bir gün önce",
            reference_date=date(2026, 7, 23),
        )
        day_before_yesterday, label = parse_target_date_tr(
            "Evveli gün",
            reference_date=date(2026, 7, 23),
        )
        self.assertEqual(yesterday, date(2026, 7, 22))
        self.assertEqual(day_before_yesterday, date(2026, 7, 21))
        self.assertEqual(label, "Evvelsi gün")

    def test_past_calendar_day_is_not_silently_moved_to_next_year(self) -> None:
        value, _ = parse_target_date_tr(
            "22 Temmuz",
            reference_date=date(2026, 7, 23),
        )
        self.assertEqual(value, date(2026, 7, 22))

    def test_explicit_future_year_is_preserved(self) -> None:
        value, _ = parse_target_date_tr(
            "22 Temmuz 2027",
            reference_date=date(2026, 7, 23),
        )
        self.assertEqual(value, date(2027, 7, 22))
