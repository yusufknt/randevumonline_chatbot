from __future__ import annotations

import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.voice.audio_socket import AudioSocketCall
from app.voice.fastagi import handle_fastagi
from app.voice.registry import registry


class _Writer:
    def __init__(self) -> None:
        self.writes: list[bytes] = []
        self.closed = False

    def write(self, data: bytes) -> None:
        self.writes.append(data)

    async def drain(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        return None


class _TwoFrameTTS:
    async def synthesize_stream(self, _text: str):
        yield b"\x01" * 320
        yield b"\x02" * 320


class VoiceHangupTests(unittest.IsolatedAsyncioTestCase):
    async def test_audiosocket_terminate_is_after_all_final_tts_frames(self) -> None:
        writer = _Writer()
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            writer,
        )
        call.dialog = SimpleNamespace(closed=True)

        with patch("app.voice.audio_socket.TextToSpeechEngine", _TwoFrameTTS):
            await call._speak("İyi günler.", asyncio.get_running_loop().time())

        packet_types = [frame[0] for frame in writer.writes]
        self.assertEqual(packet_types, [0x10, 0x10, 0x00])
        self.assertTrue(writer.closed)
        self.assertEqual(call.result, "assistant_hangup")

    async def test_fastagi_hangs_up_the_same_asterisk_channel(self) -> None:
        reader = asyncio.StreamReader()
        reader.feed_data(
            b"agi_channel: PJSIP/netgsm-endpoint-00000042\n"
            b"agi_callerid: 905551112233\n"
            b"agi_extension: 8500000000\n\n"
            b"200 result=0\n"
            b"200 result=1\n"
        )
        reader.feed_eof()
        writer = _Writer()

        await handle_fastagi(reader, writer)

        commands = b"".join(writer.writes)
        self.assertIn(b"EXEC AudioSocket ", commands)
        self.assertIn(
            b"HANGUP PJSIP/netgsm-endpoint-00000042\n", commands
        )

        # Testte gerçek AudioSocket bağlantısı kurulmadığı için oluşturulan
        # registry kaydını test sonunda elle kaldır.
        audio_command = next(
            item for item in writer.writes if item.startswith(b"EXEC AudioSocket ")
        )
        call_uuid = audio_command.split()[2].split(b",", 1)[0].decode()
        await registry.remove(call_uuid)


if __name__ == "__main__":
    unittest.main()
