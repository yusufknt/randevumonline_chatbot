from __future__ import annotations

import asyncio
import contextlib
import logging
from asyncio.subprocess import PIPE
from pathlib import Path
from typing import AsyncIterable, AsyncIterator

import httpx

from app.voice.config import VoiceSettings, get_voice_settings

log = logging.getLogger(__name__)


class TextToSpeechEngine:
    """Mevcut Voice API sesini değiştirmeden PCM olarak yayınlayan motor."""

    _client: httpx.AsyncClient | None = None

    @classmethod
    async def startup(cls) -> None:
        if cls._client is None:
            cls._client = httpx.AsyncClient(
                timeout=httpx.Timeout(connect=5, read=60, write=10, pool=5),
                limits=httpx.Limits(max_connections=6, max_keepalive_connections=3),
                http2=False,
            )

    @classmethod
    async def shutdown(cls) -> None:
        if cls._client:
            await cls._client.aclose()
            cls._client = None

    @staticmethod
    def _auth(settings: VoiceSettings) -> tuple[dict[str, str], dict[str, str]]:
        cookie_file = (
            Path(settings.tts_cookie_file).expanduser()
            if settings.tts_cookie_file else None
        )
        if cookie_file and cookie_file.is_file():
            # Netscape cookie dosyasından yalnızca gerekli cookie çifti okunur.
            cookies: dict[str, str] = {}
            for line in cookie_file.read_text(errors="ignore").splitlines():
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) >= 7:
                    cookies[parts[-2]] = parts[-1]
            if cookies:
                return {}, cookies
        if settings.tts_api_key:
            return {}, {"authorization": settings.tts_api_key}
        raise RuntimeError("TTS kimlik doğrulaması eksik")

    @staticmethod
    def _payload(text: str, settings: VoiceSettings) -> dict:
        # Mevcut createvoice/stream sözleşmesi bilerek aynen korunuyor.
        return {
            "metin": text,
            "language": "tr",
            "cinsiyet": settings.tts_api_gender,
            "sestype": settings.tts_api_emotion,
            "exaggeration": 0.5,
            "cfg_weight": 0.5,
            "temperature": 0.8,
        }

    async def _voice_api_audio(
        self, text: str, settings: VoiceSettings
    ) -> AsyncIterator[bytes]:
        await self.startup()
        assert self._client is not None
        headers, cookies = self._auth(settings)
        url = f"{settings.tts_api_base_url.rstrip('/')}/createvoice/stream"
        request = self._client.build_request(
            "POST",
            url,
            headers=headers,
            cookies=cookies,
            json=self._payload(text, settings),
        )
        response = await self._client.send(request, stream=True)
        try:
            response.raise_for_status()
            async for chunk in response.aiter_bytes(4096):
                if chunk:
                    yield chunk
        finally:
            await response.aclose()

    @staticmethod
    async def _decode_mp3(source: AsyncIterable[bytes]) -> AsyncIterator[bytes]:
        """MP3 byte akışını AudioSocket'un 8 kHz signed-linear biçimine çevirir."""
        ffmpeg = await asyncio.create_subprocess_exec(
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-f", "mp3", "-i", "pipe:0",
            "-f", "s16le", "-ar", "8000", "-ac", "1", "pipe:1",
            stdin=PIPE, stdout=PIPE, stderr=asyncio.subprocess.DEVNULL,
        )
        feed_task: asyncio.Task | None = None
        try:
            async def feed() -> None:
                try:
                    async for chunk in source:
                        if ffmpeg.stdin is None:
                            break
                        ffmpeg.stdin.write(chunk)
                        await ffmpeg.stdin.drain()
                finally:
                    if ffmpeg.stdin:
                        ffmpeg.stdin.close()

            feed_task = asyncio.create_task(feed())
            assert ffmpeg.stdout is not None
            buffer = bytearray()
            while True:
                chunk = await ffmpeg.stdout.read(320 - len(buffer))
                if not chunk:
                    break
                buffer.extend(chunk)
                if len(buffer) == 320:
                    yield bytes(buffer)
                    buffer.clear()
            if buffer:
                buffer.extend(b"\x00" * (320 - len(buffer)))
                yield bytes(buffer)
            await feed_task
            code = await ffmpeg.wait()
            if code != 0:
                raise RuntimeError(f"TTS dönüştürme başarısız code={code}")
        finally:
            if feed_task and not feed_task.done():
                feed_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await feed_task
            if ffmpeg.returncode is None:
                ffmpeg.kill()
            with contextlib.suppress(Exception):
                await ffmpeg.wait()

    async def synthesize_stream(self, text: str) -> AsyncIterator[bytes]:
        if not text.strip():
            return
        settings = get_voice_settings()

        # Upstream bazen yalnızca ID3 başlığı gönderip chunked gövdeyi yarıda
        # kapatıyor. Farklı bir konuşmacı sesi kullanmak marka sesini bozduğu
        # için yalnızca yapılandırılmış ana sağlayıcıya istek yapılır.
        for attempt in (1,):
            emitted = 0
            try:
                async for chunk in self._decode_mp3(
                    self._voice_api_audio(text, settings)
                ):
                    emitted += 1
                    yield chunk
                if emitted:
                    return
            except (httpx.HTTPError, OSError, RuntimeError) as exc:
                if emitted:
                    log.warning(
                        "Voice API ses gövdesi kısmi kapandı; üretilen PCM korundu "
                        "type=%s chunks=%d",
                        type(exc).__name__,
                        emitted,
                    )
                    return
                log.warning(
                    "Voice API ses üretmedi attempt=%d type=%s",
                    attempt,
                    type(exc).__name__,
                )

        log.error(
            "Voice API kullanılamıyor; farklı konuşmacı sesi yedeği devre dışı"
        )
