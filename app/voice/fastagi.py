from __future__ import annotations

import asyncio
import contextlib
import logging
import uuid
from urllib.parse import unquote

from app.voice.config import get_voice_settings
from app.voice.identity import normalize_phone, redact_phone
from app.voice.registry import CallContext, registry

log = logging.getLogger(__name__)


async def _read_environment(reader: asyncio.StreamReader) -> dict[str, str]:
    env: dict[str, str] = {}
    while True:
        line = await asyncio.wait_for(reader.readline(), timeout=5)
        if not line or line in {b"\n", b"\r\n"}:
            return env
        text = line.decode("utf-8", "replace").strip()
        if ":" in text:
            key, value = text.split(":", 1)
            env[key.strip()] = unquote(value.strip())


async def handle_fastagi(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    call_uuid = str(uuid.uuid4())
    try:
        env = await _read_environment(reader)
        caller = normalize_phone(
            env.get("agi_callerid") or env.get("agi_callingpres")
        )
        if not caller:
            caller = f"anonymous:{call_uuid[:12]}"
        did = normalize_phone(
            env.get("agi_extension") or env.get("agi_dnid") or env.get("agi_rdnis")
        )
        uniqueid = env.get("agi_uniqueid", call_uuid)
        await registry.put(CallContext(call_uuid, caller, did, uniqueid))
        log.info(
            "FastAGI çağrı kabul edildi uuid=%s caller=%s did=%s",
            call_uuid,
            redact_phone(caller),
            redact_phone(did),
        )
        settings = get_voice_settings()
        channel = env.get("agi_channel", "").strip()
        command = (
            f"EXEC AudioSocket {call_uuid},"
            f"{settings.voice_audiosocket_host}:{settings.voice_audiosocket_port}\n"
        )
        writer.write(command.encode())
        await writer.drain()
        # EXEC AudioSocket çağrı sona erene kadar dönmez. Burada kısa timeout
        # kullanmak aktif çağrıyı keser; TCP kapanışı doğal yaşam süresi sınırıdır.
        result = await reader.readline()
        if result and not result.startswith(b"200 result="):
            log.error("AudioSocket AGI başlatılamadı uuid=%s", call_uuid)
            await registry.remove(call_uuid)
        elif result:
            # AudioSocket sunucusu kapanış anonsundan sonra döndüğünde kanalı
            # açık bırakma; dialplan Hangup'a ek olarak AGI seviyesinde de kapat.
            hangup_command = f"HANGUP {channel}\n" if channel else "HANGUP\n"
            writer.write(hangup_command.encode())
            await writer.drain()
            try:
                hangup_result = await asyncio.wait_for(reader.readline(), timeout=2)
            except asyncio.TimeoutError:
                hangup_result = b""
            # Kanal karşı uç veya dialplan tarafından zaten kapandıysa Asterisk
            # FastAGI soketine doğrudan HANGUP bildirimi gönderir. Bu da başarılı
            # sonlandırmadır, komut reddi değildir.
            accepted = (
                not hangup_result
                or hangup_result.startswith(b"200 result=1")
                or hangup_result.strip() == b"HANGUP"
            )
            if accepted:
                log.info("FastAGI HANGUP kabul edildi uuid=%s", call_uuid)
            else:
                log.error(
                    "FastAGI HANGUP reddedildi uuid=%s response=%s",
                    call_uuid,
                    hangup_result.decode("utf-8", "replace").strip()[:80],
                )
        elif not result:
            log.info("FastAGI kanal tarafından kapatıldı uuid=%s", call_uuid)
    except (ConnectionError, asyncio.IncompleteReadError) as exc:
        log.warning("FastAGI bağlantısı kapandı uuid=%s type=%s", call_uuid, type(exc).__name__)
        await registry.remove(call_uuid)
    except Exception:
        log.exception("FastAGI işleme hatası uuid=%s", call_uuid)
        await registry.remove(call_uuid)
    finally:
        writer.close()
        await writer.wait_closed()


async def start_fastagi() -> asyncio.Server:
    settings = get_voice_settings()
    return await asyncio.start_server(
        handle_fastagi, settings.voice_agi_host, settings.voice_agi_port
    )
