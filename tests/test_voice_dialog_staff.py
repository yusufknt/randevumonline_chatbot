from __future__ import annotations

import unittest
from datetime import date

from app.voice.dialog import (
    DialogManager,
    Pending,
    _repair_date_stt,
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

    async def test_staff_question_uses_barber_word_and_first_names(self) -> None:
        answer = await self.dialog.respond("Randevu almak istiyorum")
        self.assertEqual(
            answer,
            "Uygun berberlerimiz: Mehmet, Yusuf, Ahmet ve Emre. "
            "Hangi berberi tercih edersiniz?",
        )

    async def test_first_name_advances_booking_without_llm(self) -> None:
        answer = await self.dialog.respond("Emre")
        self.assertEqual(self.dialog.staff_member["name"], "Emre Şahin")
        self.assertEqual(answer, "Hangi hizmeti istersiniz? Saç Kesimi.")

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
        self.assertEqual(self.dialog.target_date, date(2026, 7, 21))
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertIsNone(self.dialog.service)
        self.assertEqual(answer, "Hangi hizmeti istersiniz? Saç Kesimi.")

    async def test_complete_mixed_order_sentence_goes_to_confirmation(self) -> None:
        answer = await self.dialog.respond(
            "Saat 5'e Mehmet Bey'den yarın saç kesimi alacağım."
        )

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        self.assertEqual(self.dialog.target_date, date(2026, 7, 21))
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertEqual(self.dialog.pending.action, "create")
        self.assertEqual(
            answer,
            "21 Temmuz saat 17:00, Mehmet Kaya, Saç Kesimi için "
            "randevuyu onaylıyor musunuz?",
        )

    async def test_common_phone_stt_variant_yarim_is_repaired_in_booking(self) -> None:
        answer = await self.dialog.respond(
            "Mehmet Beyden saat beşe alacağım, yarım."
        )

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.target_date, date(2026, 7, 21))
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertEqual(answer, "Hangi hizmeti istersiniz? Saç Kesimi.")
