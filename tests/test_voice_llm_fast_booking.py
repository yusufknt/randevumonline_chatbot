from __future__ import annotations

import json
import unittest
from datetime import date
from unittest.mock import AsyncMock, patch

from app.voice.llm import VoiceLLMEngine
from app.voice.tools import VoiceToolExecutor


async def collect_response(engine: VoiceLLMEngine, text: str) -> str:
    chunks = [chunk async for chunk in engine.generate_response(text)]
    return " ".join(chunks)


class FakeStreamResponse:
    def __init__(self, content: str) -> None:
        self.content = content

    async def __aenter__(self) -> "FakeStreamResponse":
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None:
        return None

    def raise_for_status(self) -> None:
        return None

    async def aiter_lines(self):
        payload = {"choices": [{"delta": {"content": self.content}}]}
        yield f"data: {json.dumps(payload)}"
        yield "data: [DONE]"


class FakeLLMClient:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses
        self.requests: list[dict] = []

    def stream(self, method: str, url: str, **kwargs):
        self.requests.append(kwargs["json"])
        return FakeStreamResponse(self.responses.pop(0))


class VoiceLLMFastBookingTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.patches = [
            patch.object(
                VoiceToolExecutor,
                "get_services",
                AsyncMock(
                    side_effect=[
                        "Mehmet ustanın yaptığı işlemler: Saç Kesimi, Sakal Tıraşı",
                        ["Saç Kesimi", "Sakal Tıraşı"],
                    ]
                ),
            ),
            patch.object(
                VoiceToolExecutor,
                "get_staff",
                AsyncMock(return_value=["Yusuf Demir", "Mehmet Kaya"]),
            ),
            patch.object(
                VoiceToolExecutor,
                "get_business_info",
                AsyncMock(return_value={"name": "Berber Mehmet"}),
            ),
            patch.object(
                VoiceToolExecutor,
                "get_customer_appointments",
                AsyncMock(return_value=[]),
            ),
            patch.object(
                VoiceToolExecutor,
                "check_availability",
                AsyncMock(return_value={"available_slots": ["15:00", "17:00"]}),
            ),
            patch.object(
                VoiceToolExecutor,
                "book_appointment",
                AsyncMock(return_value={"appointment_id": "test-id"}),
            ),
        ]
        for item in self.patches:
            item.start()

    def tearDown(self) -> None:
        for item in reversed(self.patches):
            item.stop()

    async def test_clear_farewell_closes_before_database_or_llm(self) -> None:
        engine = VoiceLLMEngine()

        response = await collect_response(engine, "Yok, teşekkür ederim.")

        self.assertTrue(engine.is_session_closed)
        self.assertIn("İyi günler", response)
        VoiceToolExecutor.get_services.assert_not_awaited()
        VoiceToolExecutor.get_staff.assert_not_awaited()

    async def test_close_keywords_cover_natural_call_endings(self) -> None:
        for text in (
            "Başka bir isteğim yok.",
            "Bu kadar.",
            "Telefonu kapatabilirsin.",
            "Tamamdır, iyi günler.",
            "Görüşürüz.",
        ):
            with self.subTest(text=text):
                engine = VoiceLLMEngine()
                await collect_response(engine, text)
                self.assertTrue(engine.is_session_closed)

    async def test_complete_sentence_books_without_second_llm_turn(self) -> None:
        engine = VoiceLLMEngine()
        target_year = date.today().year + 1
        fake_llm = FakeLLMClient(
            [
                f"[RANDEVU: {target_year}-07-18 17:00 | Mehmet Kaya | "
                "Saç Kesimi | Telefon Müşterisi]"
            ]
        )
        engine._http_client = fake_llm

        response = await collect_response(
            engine,
            f"18 Temmuz {target_year} saat 17'de Mehmet Kaya'ya "
            "saç kesimi randevusu almak istiyorum.",
        )

        self.assertIn("oluşturuldu", response)
        self.assertNotIn("saat saat", response.lower())
        VoiceToolExecutor.book_appointment.assert_awaited_once()
        call = VoiceToolExecutor.book_appointment.await_args.kwargs
        self.assertEqual(call["start_time_local"], f"{target_year}-07-18 17:00")
        self.assertEqual(call["staff_name"], "Mehmet Kaya")
        self.assertEqual(call["service_name"], "Saç Kesimi")
        VoiceToolExecutor.check_availability.assert_not_awaited()
        self.assertEqual(len(fake_llm.requests), 1)
        memory_message = fake_llm.requests[0]["messages"][-2]["content"]
        self.assertIn("Usta: Mehmet Kaya", memory_message)
        self.assertIn(f"Tarih: {target_year}-07-18", memory_message)
        self.assertIn("Saat: 17:00", memory_message)

    async def test_time_is_remembered_while_only_missing_service_is_asked(self) -> None:
        engine = VoiceLLMEngine()
        target_year = date.today().year + 1
        fake_llm = FakeLLMClient(
            [
                f"[RANDEVU: {target_year}-07-18 17:00 | Mehmet Kaya | "
                "Saç Kesimi | Telefon Müşterisi]",
            ]
        )
        engine._http_client = fake_llm

        first_response = await collect_response(
            engine,
            f"18 Temmuz {target_year} saat 17'de Mehmet Kaya'ya "
            "randevu almak istiyorum.",
        )

        self.assertIn("hangi işlemi", first_response.lower())
        self.assertNotIn("hangi saat", first_response.lower())
        self.assertEqual(engine.memory_time, "17:00")
        VoiceToolExecutor.book_appointment.assert_not_awaited()

        second_response = await collect_response(engine, "Saç kesimi.")

        self.assertIn("oluşturuldu", second_response)
        call = VoiceToolExecutor.book_appointment.await_args.kwargs
        self.assertEqual(call["start_time_local"], f"{target_year}-07-18 17:00")
        self.assertEqual(len(fake_llm.requests), 1)


if __name__ == "__main__":
    unittest.main()
