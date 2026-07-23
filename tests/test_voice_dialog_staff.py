from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

from app.core.session_cache import HybridVoiceSessionCache
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
        self.dialog._cache = HybridVoiceSessionCache(redis_url="")
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
        self.dialog.clear_cache()
        self.slot_status_patch.stop()
        self.interpret_patch.stop()

    def test_matches_staff_by_first_name_only(self) -> None:
        self.assertEqual(self.dialog._match("Mehmet", self.dialog.staff)["_id"], "m")
        self.assertEqual(
            self.dialog._match("Emre'den randevu istiyorum", self.dialog.staff)["_id"],
            "e",
        )

    def test_matches_noisy_service_inside_a_complete_phone_sentence(self) -> None:
        self.dialog.services.extend([
            {"_id": "sk", "name": "Sakal Tıraşı"},
            {"_id": "cs", "name": "Çocuk Saç Kesimi"},
        ])

        matched = self.dialog._match(
            "Yarın Ahmet Bey'den saç kesim randomsı almak istiyorum saat 11'e",
            self.dialog.services,
        )

        self.assertIsNotNone(matched)
        self.assertEqual(matched["name"], "Saç Kesimi")

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
        self.assertEqual(
            _time_from_text(
                "Tamam, on altı otuz alayım ben.",
                allow_bare=True,
            ),
            "16:30",
        )
        self.assertEqual(
            _time_from_text("Dört buçuk olsun.", allow_bare=True),
            "16:30",
        )
        self.assertIsNone(_time_from_text("Bir randevu istiyorum"))
        self.assertIsNone(_time_from_text("Saat 28"))
        self.assertIsNone(_time_from_text("Saat 24"))
        self.assertIsNone(_time_from_text("Saat 12:75"))

    async def test_impossible_calendar_date_is_rejected_without_fallback(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]

        answer = await self.dialog.respond("32 Temmuz saat 15")

        self.assertIsNone(self.dialog.target_date)
        self.assertIsNone(self.dialog.target_time)
        self.assertIsNone(self.dialog.pending)
        self.assertIn("takvimde bulunmuyor", answer)

    async def test_out_of_range_numeric_and_spoken_hours_are_rejected(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)

        numeric_answer = await self.dialog.respond("Saat 28")
        self.assertIsNone(self.dialog.target_time)
        self.assertIn("saat geçerli değil", numeric_answer)

        spoken_answer = await self.dialog.respond("Saat yirmi sekiz")
        self.assertIsNone(self.dialog.target_time)
        self.assertIn("saat geçerli değil", spoken_answer)

        minute_answer = await self.dialog.respond("Saat 12:75")
        self.assertIsNone(self.dialog.target_time)
        self.assertIn("saat geçerli değil", minute_answer)

    async def test_invalid_time_cannot_confirm_an_existing_booking(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog.target_time = "17:00"
        self.dialog.pending = Pending("create")

        answer = await self.dialog.respond("Evet, saat 28")

        self.assertIsNone(self.dialog.target_time)
        self.assertIsNone(self.dialog.pending)
        self.assertIn("saat geçerli değil", answer)

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
        self.assertIn(
            "Saç Kesimi",
            self.dialog.normalize_stt_text(
                "Yusuf Bey'den yarın saç trafiği için boş saatleri soruyorum."
            ),
        )
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

    def test_service_barge_in_repairs_observed_kesisim_transcript(self) -> None:
        self.dialog.services.append(
            {"_id": "child", "name": "Çocuk Saç Kesimi"}
        )
        self.dialog.staff[0]["service_ids"].append("child")
        self.dialog.staff_member = self.dialog.staff[0]

        normalized = self.dialog.normalize_stt_text("Kesişim.")

        self.assertEqual(normalized, "Saç Kesimi.")
        self.assertTrue(self.dialog.accepts_low_confidence_transcript(normalized))
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript(normalized),
            "Saç Kesimi",
        )

    def test_low_confidence_text_only_accepts_and_keeps_expected_entity(self) -> None:
        noisy = "Mehmet Beydar, Landauvar, Nexturus, Buginci."
        self.assertTrue(self.dialog.accepts_low_confidence_transcript(noisy))
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript(noisy), "Mehmet Kaya"
        )
        self.assertFalse(
            self.dialog.accepts_low_confidence_transcript(
                "Evet, çok teşekkür ederim."
            )
        )
        self.assertTrue(
            self.dialog.accepts_low_confidence_transcript(
                "Kapat yigin, ne da kaldı bir şey stemmen."
            )
        )
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript(
                "Kapat yigin, ne da kaldı bir şey stemmen."
            ),
            "kapat",
        )

        self.dialog.staff_member = self.dialog.staff[0]
        self.assertTrue(
            self.dialog.accepts_low_confidence_transcript("Saç Kesimi, Sakal")
        )
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript("Saç Kesimi, Sakal"),
            "Saç Kesimi",
        )

    def test_low_confidence_confirmation_cannot_invent_a_destructive_action(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog.target_time = "17:00"
        self.dialog.pending = Pending("create")

        self.assertFalse(
            self.dialog.accepts_low_confidence_transcript("Takkatur i slot")
        )
        self.assertTrue(self.dialog.accepts_low_confidence_transcript("Evet"))
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript("Evet, onaylıyorum"),
            "evet",
        )

    def test_low_confidence_exact_time_is_accepted_but_ambiguous_time_is_not(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)

        self.assertTrue(self.dialog.accepts_low_confidence_transcript("On iki"))
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript("On iki"),
            "saat 12:00",
        )
        self.assertFalse(
            self.dialog.accepts_low_confidence_transcript(
                "Saat iki, saat on iki"
            )
        )

    def test_low_confidence_prompt_reasks_current_field_without_error_phrase(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.assertEqual(
            self.dialog.low_confidence_retry_prompt(),
            "Hangi hizmeti istediğinizi tekrar söyler misiniz?",
        )
        self.assertNotIn(
            "net duyamadım", self.dialog.low_confidence_retry_prompt().lower()
        )

    def test_interruption_retry_does_not_repeat_the_stopped_list(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]

        prompt = self.dialog.interruption_retry_prompt()

        self.assertEqual(
            prompt,
            "Sizi dinliyorum; hangi hizmeti istediğinizi söyler misiniz?",
        )
        self.assertNotIn("hizmetlerimiz", prompt.casefold())

    def test_low_confidence_spoken_explicit_date_keeps_new_date(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date(2026, 7, 24)

        normalized = self.dialog.normalize_stt_text("Otuz Ağustos.")

        self.assertEqual(normalized, "30 Ağustos.")
        self.assertTrue(self.dialog.accepts_low_confidence_transcript(normalized))
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript(normalized),
            "30 Ağustos",
        )

    def test_low_confidence_relative_date_is_actionable(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]

        normalized = self.dialog.normalize_stt_text("Üç gün sonra.")

        self.assertTrue(self.dialog.accepts_low_confidence_transcript(normalized))
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript(normalized),
            _date_spoken(date.today() + timedelta(days=3)),
        )

    async def test_staff_question_uses_barber_word_and_first_names(self) -> None:
        self.assertEqual(
            self.dialog.opening_prompt(),
            "Berberlerimiz: Mehmet, Yusuf, Ahmet ve Emre. Hangisini tercih edersiniz?",
        )
        answer = await self.dialog.respond("Randevu almak istiyorum")
        self.assertEqual(
            answer,
            "Berberlerimiz: Mehmet, Yusuf, Ahmet ve Emre. Hangisini tercih edersiniz?",
        )

    async def test_first_name_advances_booking_without_llm(self) -> None:
        answer = await self.dialog.respond("Emre")
        self.assertEqual(self.dialog.staff_member["name"], "Emre Şahin")
        self.assertEqual(answer, "Hizmetlerimiz: Saç Kesimi. Hangisini istersiniz?")

    async def test_no_staff_preference_selects_real_compatible_staff(self) -> None:
        answer = await self.dialog.respond("Fark etmez, siz seçin.")

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(answer, "Hizmetlerimiz: Saç Kesimi. Hangisini istersiniz?")
        self.dialog._interpret.assert_not_awaited()

    async def test_no_staff_preference_keeps_previous_booking_details(self) -> None:
        tomorrow = date.today() + timedelta(days=1)

        await self.dialog.respond("Yarın saç kesimi saat beş")
        answer = await self.dialog.respond("Kim müsaitse olur")

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        self.assertEqual(self.dialog.target_date, tomorrow)
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertIn("onaylıyor musunuz", answer)

    async def test_earliest_available_time_advances_to_confirmation(self) -> None:
        tz = ZoneInfo("Europe/Istanbul")
        self.dialog.business["timezone"] = "Europe/Istanbul"
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = {
            **self.dialog.services[0],
            "duration_minutes": 30,
        }
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog._available_slots = AsyncMock(return_value=[
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=11),
                tzinfo=tz,
            ),
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=9),
                tzinfo=tz,
            ),
        ])

        answer = await self.dialog.respond("En erken saat olsun")

        self.assertEqual(self.dialog.target_time, "09:00")
        self.assertIn("saat 09:00", answer)
        self.assertIn("onaylıyor musunuz", answer)

    async def test_spoken_staff_and_service_advance_without_finishing_lists(self) -> None:
        staff_answer = await self.dialog.respond("Yusuf")
        self.assertEqual(self.dialog.staff_member["name"], "Yusuf Demir")
        self.assertEqual(
            staff_answer,
            "Hizmetlerimiz: Saç Kesimi. Hangisini istersiniz?",
        )

        service_answer = await self.dialog.respond("Saç kesimi")
        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        self.assertEqual(service_answer, "Hangi gün gelmek istersiniz?")

    async def test_partial_hair_transcript_only_lists_matching_services(self) -> None:
        self.dialog.services.extend([
            {"_id": "combo", "name": "Saç + Sakal"},
            {"_id": "child", "name": "Çocuk Saç Kesimi"},
            {"_id": "beard", "name": "Sakal Tıraşı"},
        ])
        self.dialog.staff[0]["service_ids"].extend(["combo", "child", "beard"])
        self.dialog.staff_member = self.dialog.staff[0]

        answer = await self.dialog.respond("Saç")

        self.assertIsNone(self.dialog.service)
        self.assertIn("Saç Kesimi", answer)
        self.assertIn("Saç + Sakal", answer)
        self.assertIn("Çocuk Saç Kesimi", answer)
        self.assertNotIn("Sakal Tıraşı", answer)
        self.dialog._interpret.assert_not_awaited()

    async def test_exact_hair_service_still_advances_normally(self) -> None:
        self.dialog.services.extend([
            {"_id": "combo", "name": "Saç + Sakal"},
            {"_id": "child", "name": "Çocuk Saç Kesimi"},
        ])
        self.dialog.staff[0]["service_ids"].extend(["combo", "child"])
        self.dialog.staff_member = self.dialog.staff[0]

        answer = await self.dialog.respond("Saç kesimi")

        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        self.assertEqual(answer, "Hangi gün gelmek istersiniz?")

    def test_low_confidence_partial_hair_is_kept_for_clarification(self) -> None:
        self.dialog.services.extend([
            {"_id": "combo", "name": "Saç + Sakal"},
            {"_id": "child", "name": "Çocuk Saç Kesimi"},
        ])
        self.dialog.staff[0]["service_ids"].extend(["combo", "child"])
        self.dialog.staff_member = self.dialog.staff[0]

        self.assertTrue(self.dialog.accepts_low_confidence_transcript("Saç"))
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript("Saç"),
            "saç",
        )

    async def test_unknown_spoken_staff_lists_only_real_staff(self) -> None:
        answer = await self.dialog.respond("Fırat usta")

        self.assertIsNone(self.dialog.staff_member)
        self.assertIn("Fırat isimli bir ustamız bulunmuyor", answer)
        for first_name in ("Mehmet", "Yusuf", "Ahmet", "Emre"):
            self.assertIn(first_name, answer)
        self.dialog._interpret.assert_not_awaited()

    def test_low_confidence_unknown_staff_reaches_catalog_clarification(self) -> None:
        self.assertTrue(
            self.dialog.accepts_low_confidence_transcript("Fırat usta")
        )
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript("Fırat usta"),
            "Fırat usta",
        )

    async def test_unknown_staff_correction_cannot_keep_previous_staff(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog.target_time = "17:00"

        answer = await self.dialog.respond("Fırat ustadan olsun")

        self.assertIsNone(self.dialog.staff_member)
        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        self.assertIn("Ustalarımız", answer)
        self.assertNotIn("onaylıyor musunuz", answer)

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
        self.assertEqual(answer, "Hizmetlerimiz: Saç Kesimi. Hangisini istersiniz?")

    async def test_complete_mixed_order_sentence_creates_without_confirmation(self) -> None:
        self.dialog.customer = {"_id": "customer"}
        self.dialog.conversation = {"_id": "conversation"}
        tomorrow = date.today() + timedelta(days=1)
        create = AsyncMock(return_value={"appointment_id": "appointment"})

        with patch("app.voice.dialog.create_appointment", create):
            answer = await self.dialog.respond(
                "Saat 5'e Mehmet Bey'den yarın saç kesimi alacağım."
            )

        self.assertEqual(
            answer,
            "Randevunuz oluşturuldu. Başka bir isteğiniz var mı?",
        )
        self.assertEqual(self.dialog.pending.action, "post_booking")
        self.assertNotIn("onay", answer.casefold())
        create.assert_awaited_once()
        kwargs = create.await_args.kwargs
        self.assertEqual(kwargs["staff"]["name"], "Mehmet Kaya")
        self.assertEqual(kwargs["service"]["name"], "Saç Kesimi")
        self.assertEqual(kwargs["start_local"], f"{tomorrow.isoformat()} 17:00")

    async def test_ahmet_beard_service_full_sentence_creates_immediately(self) -> None:
        beard = {"_id": "sk", "name": "Sakal Tıraşı"}
        self.dialog.services.append(beard)
        self.dialog.staff[2]["service_ids"].append("sk")
        self.dialog.customer = {"_id": "customer"}
        self.dialog.conversation = {"_id": "conversation"}
        tomorrow = date.today() + timedelta(days=1)
        create = AsyncMock(return_value={"appointment_id": "appointment"})

        with patch("app.voice.dialog.create_appointment", create):
            answer = await self.dialog.respond(
                "Ahmet Bey'den yarın saat on ikide sakal tıraşı randevusu istiyorum"
            )

        self.assertEqual(
            answer, "Randevunuz oluşturuldu. Başka bir isteğiniz var mı?"
        )
        self.assertEqual(self.dialog.pending.action, "post_booking")
        kwargs = create.await_args.kwargs
        self.assertEqual(kwargs["staff"]["name"], "Ahmet Yılmaz")
        self.assertEqual(kwargs["service"]["name"], "Sakal Tıraşı")
        self.assertEqual(kwargs["start_local"], f"{tomorrow.isoformat()} 12:00")

    async def test_noisy_complete_phone_sentence_creates_without_confirmation(self) -> None:
        self.dialog.customer = {"_id": "customer"}
        self.dialog.conversation = {"_id": "conversation"}
        tomorrow = date.today() + timedelta(days=1)
        create = AsyncMock(return_value={"appointment_id": "appointment"})

        with patch("app.voice.dialog.create_appointment", create):
            answer = await self.dialog.respond(
                "Yarın için Ahmet Bey'den saç kesim randomsı almak "
                "istiyorum saat 11'e."
            )

        self.assertEqual(
            answer, "Randevunuz oluşturuldu. Başka bir isteğiniz var mı?"
        )
        self.assertNotIn("onay", answer.casefold())
        kwargs = create.await_args.kwargs
        self.assertEqual(kwargs["staff"]["name"], "Ahmet Yılmaz")
        self.assertEqual(kwargs["service"]["name"], "Saç Kesimi")
        self.assertEqual(kwargs["start_local"], f"{tomorrow.isoformat()} 11:00")

    async def test_partial_out_of_order_details_only_ask_what_is_missing(self) -> None:
        tomorrow = date.today() + timedelta(days=1)

        self.assertIn("Berberlerimiz", await self.dialog.respond("Saç kesimi"))
        self.assertIn("Berberlerimiz", await self.dialog.respond("Yarın"))
        answer = await self.dialog.respond("Mehmet saat beş")

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        self.assertEqual(self.dialog.target_date, tomorrow)
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertIn("onaylıyor musunuz", answer)

    async def test_service_not_offered_by_selected_staff_is_not_confirmed(self) -> None:
        incompatible = {"_id": "other", "name": "Saç Boyası"}
        self.dialog.services.append(incompatible)

        answer = await self.dialog.respond(
            "Mehmet saç boyası yarın saat beş randevu"
        )

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertIsNone(self.dialog.service)
        self.assertIn("Hizmetlerimiz", answer)
        self.assertNotIn("onaylıyor musunuz", answer)

    async def test_common_phone_stt_variant_yarim_is_repaired_in_booking(self) -> None:
        answer = await self.dialog.respond(
            "Mehmet Beyden saat beşe alacağım, yarım."
        )

        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.target_date, date.today() + timedelta(days=1))
        self.assertEqual(self.dialog.target_time, "17:00")
        self.assertEqual(answer, "Hizmetlerimiz: Saç Kesimi. Hangisini istersiniz?")

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

    async def test_successful_booking_waits_for_another_request(self) -> None:
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
        self.assertEqual(
            answer, "Randevunuz oluşturuldu. Başka bir isteğiniz var mı?"
        )
        self.assertIsNone(self.dialog.completion_kind)

        farewell = await self.dialog.respond("Yok teşekkürler")
        self.assertTrue(self.dialog.closed)
        self.assertIn("İyi günler", farewell)

    async def test_turkish_capital_i_farewell_closes_from_any_step(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]

        farewell = await self.dialog.respond("İyi günler, kolay gelsin.")

        self.assertTrue(self.dialog.closed)
        self.assertIn("İyi günler", farewell)

    async def test_standalone_kolay_gelsin_closes_but_request_does_not(self) -> None:
        farewell = await self.dialog.respond("Kolay gelsin.")

        self.assertTrue(self.dialog.closed)
        self.assertIn("İyi günler", farewell)

        dialog = DialogManager(
            {"name": "Randevum Online", "_id": "business"},
            "+905000000001",
            "second-call",
        )
        dialog._cache = HybridVoiceSessionCache(redis_url="")
        dialog.staff = self.dialog.staff
        dialog.services = self.dialog.services
        with patch.object(DialogManager, "_interpret", AsyncMock(return_value={})):
            answer = await dialog.respond(
                "Kolay gelsin, yarın için randevu almak istiyorum."
            )
        self.assertFalse(dialog.closed)
        self.assertIn("Berberlerimiz", answer)
        dialog.clear_cache()

    async def test_successful_cancel_waits_for_another_request(self) -> None:
        self.dialog.pending = Pending("cancel", {"_id": "appointment"})

        with patch(
            "app.voice.dialog.cancel_appointment",
            AsyncMock(return_value=True),
        ):
            answer = await self.dialog.respond("Evet")

        self.assertFalse(self.dialog.closed)
        self.assertEqual(self.dialog.pending.action, "post_booking")
        self.assertEqual(answer, "Randevunuz iptal edildi. Başka bir isteğiniz var mı?")

    async def test_successful_reschedule_waits_for_another_request(self) -> None:
        self.dialog.pending = Pending(
            "reschedule_confirm", {"_id": "appointment"}
        )
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog.target_time = "17:00"

        with patch(
            "app.voice.dialog.reschedule_appointment",
            AsyncMock(return_value={"status": "rescheduled"}),
        ):
            answer = await self.dialog.respond("Evet")

        self.assertFalse(self.dialog.closed)
        self.assertEqual(self.dialog.pending.action, "post_booking")
        self.assertEqual(answer, "Randevunuz değiştirildi. Başka bir isteğiniz var mı?")

    def test_post_booking_negative_must_be_short_and_unambiguous(self) -> None:
        for phrase in (
            "Hayır",
            "Yok",
            "Hayır, yok.",
            "Hayır, yok, yok.",
            "Başka bir isteğim yok",
            "Başka bir şey yok",
            "Gerek yok",
            "İstemiyorum",
            "Sağ olun",
            "Teşekkürler",
            "Bu kadar",
            "Hepsi bu",
            "Yoktur",
        ):
            with self.subTest(phrase=phrase):
                self.assertTrue(_no_more_requests(phrase))
        self.assertTrue(
            _no_more_requests(
                "Başka bir isteğim yok, konuşmayı sonlandırabilirsin."
            )
        )
        self.assertFalse(
            _no_more_requests("Hayır yok ama arkadaşımın bilgilerini vereceğim")
        )
        self.assertFalse(
            _no_more_requests("Sağ olun, yarın için yeni randevu istiyorum")
        )

    async def test_repeated_post_booking_negative_closes_without_staff_prompt(self) -> None:
        self.dialog.pending = Pending("post_booking")

        answer = await self.dialog.respond("Hayır, yok, yok.")

        self.assertTrue(self.dialog.closed)
        self.assertIsNone(self.dialog.pending)
        self.assertIn("İyi günler", answer)
        self.assertNotIn("Berberlerimiz", answer)

    async def test_ambiguous_post_booking_answer_keeps_follow_up_state(self) -> None:
        self.dialog.pending = Pending("post_booking")

        answer = await self.dialog.respond("Hımm, bir düşüneyim")

        self.assertFalse(self.dialog.closed)
        self.assertEqual(self.dialog.pending.action, "post_booking")
        self.assertEqual(answer, "Randevunuz hazır. Başka bir isteğiniz var mı?")
        self.assertNotIn("Berberlerimiz", answer)

    async def test_explicit_new_request_after_booking_starts_second_booking(self) -> None:
        self.dialog.pending = Pending("post_booking")

        answer = await self.dialog.respond("Mehmet'ten saç kesimi istiyorum")

        self.assertFalse(self.dialog.closed)
        self.assertIsNone(self.dialog.pending)
        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.assertEqual(self.dialog.service["name"], "Saç Kesimi")
        self.assertEqual(answer, "Hangi gün gelmek istersiniz?")

    async def test_explicit_conversation_end_request_closes_dialog(self) -> None:
        answer = await self.dialog.respond(
            "Başka bir isteğim yok, konuşmayı sonlandırabilirsin."
        )

        self.assertTrue(self.dialog.closed)
        self.assertIn("İyi günler", answer)
        self.assertNotIn("Berberlerimiz", answer)

    async def test_repeated_confirmation_does_not_leave_post_booking_state(self) -> None:
        self.dialog.pending = Pending("post_booking")
        answer = await self.dialog.respond("Onaylıyorum, evet onayladım")
        self.assertFalse(self.dialog.closed)
        self.assertEqual(self.dialog.pending.action, "post_booking")
        self.assertIn("Başka bir isteğiniz", answer)

    async def test_service_step_uses_grounded_natural_llm_answer(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog._interpret = AsyncMock(
            return_value={
                "intent": "other",
                "answer": (
                    "Merhaba, elbette yardımcı olayım; Mehmet Bey için hangi "
                    "hizmeti düşünüyorsunuz?"
                ),
            }
        )
        answer = await self.dialog.respond("Merhaba")
        self.assertIn("Merhaba", answer)
        self.assertIn("hangi hizmeti", answer)
        self.assertEqual(self.dialog.staff_member["name"], "Mehmet Kaya")
        self.dialog._interpret.assert_awaited_once()

    async def test_unexpected_customer_reaction_is_not_forced_into_booking(self) -> None:
        self.dialog._interpret = AsyncMock(
            return_value={
                "intent": "other",
                "answer": (
                    "Sizi anlıyorum, içinize sinen bir seçim yapmanız önemli; "
                    "isterseniz beklentinizi söyleyin, birlikte netleştirelim."
                ),
            }
        )

        answer = await self.dialog.respond("Mehmet iyi kesiyor mu, emin olamadım")

        self.assertIn("Sizi anlıyorum", answer)
        self.assertIsNone(self.dialog.staff_member)
        self.assertIsNone(self.dialog.pending)
        self.dialog._interpret.assert_awaited_once()

    async def test_question_containing_booking_word_is_interpreted_as_a_question(self) -> None:
        self.dialog._interpret = AsyncMock(
            return_value={
                "intent": "other",
                "answer": "Hayır, randevu oluşturmak için ayrıca ücret almıyoruz.",
            }
        )

        answer = await self.dialog.respond(
            "Randevu almak için ayrıca ücret alıyor musunuz?"
        )

        self.assertIn("ayrıca ücret almıyoruz", answer)
        self.assertIsNone(self.dialog.pending)
        self.dialog._interpret.assert_awaited_once()

    async def test_other_without_llm_answer_returns_current_context_question(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog._interpret = AsyncMock(return_value={})

        answer = await self.dialog.respond("Biraz düşüneyim")

        self.assertEqual(
            answer, "Hizmetlerimiz: Saç Kesimi. Hangisini istersiniz?"
        )

    def test_llm_cannot_invent_date_or_time_without_transcript_evidence(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog._apply_entities(
            "Randevu almak istiyorum",
            {"date": date.today().isoformat(), "time": "14:00"},
        )
        self.assertIsNone(self.dialog.target_date)
        self.assertIsNone(self.dialog.target_time)

    def test_multiple_spoken_staff_names_are_recognized_as_list_echo(self) -> None:
        names = ", ".join(item["name"] for item in self.dialog.staff[:3])
        self.assertTrue(self.dialog.is_probable_playback_echo(names))
        self.assertFalse(
            self.dialog.is_probable_playback_echo(self.dialog.staff[0]["name"])
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

    async def test_availability_is_queried_once_for_day_and_time_steps(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = {
            "_id": "s",
            "name": "Saç Kesimi",
            "duration_minutes": 30,
        }
        self.dialog.target_date = date.today() + timedelta(days=1)
        tz = ZoneInfo("Europe/Istanbul")
        slots = [
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=10),
                tzinfo=tz,
            ).astimezone(timezone.utc)
        ]

        with patch(
            "app.voice.dialog.compute_available_slots",
            AsyncMock(return_value=slots),
        ) as query:
            await self.dialog._availability_answer()
            cached_slots = await self.dialog._available_slots()

        self.assertEqual(cached_slots, slots)
        query.assert_awaited_once()
        self.assertEqual(query.await_args.kwargs["step_minutes"], 45)

    def test_contiguous_slots_only_describe_real_start_times(self) -> None:
        tz = ZoneInfo("Europe/Istanbul")
        slots = [
            datetime(2026, 7, 22, hour, minute, tzinfo=tz).astimezone(timezone.utc)
            for hour, minute in (
                (11, 0), (11, 45), (12, 30), (13, 15),
            )
        ]

        ranges = _slot_ranges(slots, tz, duration_minutes=30)

        self.assertEqual(len(ranges), 1)
        self.assertEqual(
            _format_slot_ranges(ranges),
            "saat 11 ile 13:15 arası",
        )
        self.assertEqual(ranges[0][0].strftime("%H:%M"), "11:00")
        self.assertEqual(ranges[0][1].strftime("%H:%M"), "13:15")

    def test_missing_45_minute_slot_splits_spoken_blocks(self) -> None:
        tz = ZoneInfo("Europe/Istanbul")
        slots = [
            datetime(2026, 7, 22, hour, minute, tzinfo=tz).astimezone(timezone.utc)
            for hour, minute in ((11, 0), (11, 45), (13, 15))
        ]

        ranges = _slot_ranges(slots, tz, duration_minutes=30)

        self.assertEqual(len(ranges), 2)
        self.assertEqual(
            _format_slot_ranges(ranges),
            "saat 11 ile 11:45 arası ve saat 13:15",
        )

    def test_single_start_slot_does_not_speak_service_end_time(self) -> None:
        tz = ZoneInfo("Europe/Istanbul")
        slots = [
            datetime(2026, 7, 22, 11, 45, tzinfo=tz).astimezone(timezone.utc)
        ]

        ranges = _slot_ranges(slots, tz, duration_minutes=60)

        self.assertEqual(_format_slot_ranges(ranges), "saat 11:45")

    async def test_availability_answer_does_not_offer_unbookable_end_time(self) -> None:
        tz = ZoneInfo("Europe/Istanbul")
        self.dialog.business["timezone"] = "Europe/Istanbul"
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = {
            **self.dialog.services[0],
            "duration_minutes": 60,
        }
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog._available_slots = AsyncMock(return_value=[
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=11, minute=45),
                tzinfo=tz,
            ),
        ])

        answer = await self.dialog._availability_answer()

        self.assertIn("uygun alınabilecek saatler: saat 11:45", answer)
        self.assertNotIn("12:45", answer)

    async def test_spoken_sixteen_thirty_advances_to_confirmation(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)

        answer = await self.dialog.respond(
            "Tamam, on altı otuz alayım ben."
        )

        self.assertEqual(self.dialog.target_time, "16:30")
        self.assertIn("saat 16:30", answer)
        self.assertIn("onaylıyor musunuz", answer)

    async def test_afternoon_request_only_speaks_afternoon_start_slots(self) -> None:
        tz = ZoneInfo("Europe/Istanbul")
        self.dialog.business["timezone"] = "Europe/Istanbul"
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = {
            **self.dialog.services[0],
            "duration_minutes": 30,
        }
        self.dialog.target_date = date.today() + timedelta(days=1)
        self.dialog._available_slots = AsyncMock(return_value=[
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=10),
                tzinfo=tz,
            ),
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=12),
                tzinfo=tz,
            ),
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=14, minute=30),
                tzinfo=tz,
            ),
            datetime.combine(
                self.dialog.target_date,
                datetime.min.time().replace(hour=18),
                tzinfo=tz,
            ),
        ])

        answer = await self.dialog.respond("Öğleden sonra olsun")

        self.assertEqual(self.dialog.time_preference, "afternoon")
        self.assertIn("öğleden sonra", answer)
        self.assertIn("12", answer)
        self.assertIn("14:30", answer)
        self.assertNotIn("10", answer)
        self.assertNotIn("18", answer)

    def test_low_confidence_afternoon_preference_is_preserved(self) -> None:
        self.dialog.staff_member = self.dialog.staff[0]
        self.dialog.service = self.dialog.services[0]
        self.dialog.target_date = date.today() + timedelta(days=1)

        self.assertTrue(
            self.dialog.accepts_low_confidence_transcript("Öğleden sonra")
        )
        self.assertEqual(
            self.dialog.sanitize_low_confidence_transcript("Öğleden sonra"),
            "öğleden sonra",
        )
