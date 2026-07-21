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
