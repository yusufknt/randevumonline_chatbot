"""Asterisk olmadan Netgsm SIP ve RTP çağrı sahibi."""

from __future__ import annotations

import asyncio
import contextlib
import logging
import random
import re
import socket
import uuid
from dataclasses import dataclass, field

from app.voice.audio_socket import encode_frame, handle_audiosocket
from app.voice.config import get_voice_settings
from app.voice.identity import normalize_phone, redact_phone
from app.voice.registry import CallContext, registry
from app.voice.rtp_server import RTPServerProtocol

logger = logging.getLogger(__name__)

SIGNALING_KEEPALIVE_INTERVAL_SECONDS = 15.0


def _header_values(message: str, name: str) -> list[str]:
    pattern = rf"(?im)^{re.escape(name)}\s*:\s*(.+?)\s*$"
    return [value.strip() for value in re.findall(pattern, message)]


def _header(message: str, name: str, default: str = "") -> str:
    values = _header_values(message, name)
    return values[0] if values else default


def _uri_user(value: str) -> str:
    match = re.search(r"sips?:([^@;>\s]+)", value, re.IGNORECASE)
    return match.group(1) if match else ""


def _request_uri_user(message: str) -> str:
    first_line = message.splitlines()[0] if message else ""
    match = re.match(r"\S+\s+sips?:([^@;>\s]+)", first_line, re.IGNORECASE)
    return match.group(1) if match else ""


def _ensure_tag(value: str, tag: str) -> str:
    return value if re.search(r";\s*tag=", value, re.IGNORECASE) else f"{value};tag={tag}"


def _contact_uri(message: str) -> str:
    contact = _header(message, "Contact")
    match = re.search(r"<([^>]+)>", contact)
    if match:
        return match.group(1).strip()
    return contact.split(",", 1)[0].strip()


class DirectMediaWriter:
    """AudioSocket konuşma çekirdeğinin çıkışını doğrudan RTP'ye bağlar."""

    def __init__(self, on_terminate) -> None:
        self.rtp: RTPServerProtocol | None = None
        self._buffer = bytearray()
        self._on_terminate = on_terminate
        self._terminate_sent = False
        self._closed = False

    def write(self, data: bytes) -> None:
        if self._closed and not data:
            return
        self._buffer.extend(data)
        while len(self._buffer) >= 3:
            size = int.from_bytes(self._buffer[1:3], "big")
            if len(self._buffer) < size + 3:
                return
            packet_type = self._buffer[0]
            payload = bytes(self._buffer[3:size + 3])
            del self._buffer[:size + 3]
            if packet_type == 0x10 and self.rtp:
                self.rtp.send_pcm(payload)
            elif packet_type == 0x00 and not self._terminate_sent:
                self._terminate_sent = True
                result = self._on_terminate()
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)

    async def drain(self) -> None:
        await asyncio.sleep(0)

    def close(self) -> None:
        self._closed = True

    async def wait_closed(self) -> None:
        await asyncio.sleep(0)

    def is_closing(self) -> bool:
        return self._closed


@dataclass(slots=True)
class SIPCall:
    call_id: str
    call_uuid: str
    invite: str
    signaling_addr: tuple[str, int]
    local_ip: str
    local_tag: str
    reader: asyncio.StreamReader
    writer: DirectMediaWriter
    rtp_transport: asyncio.DatagramTransport
    rtp_protocol: RTPServerProtocol
    final_response: str
    task: asyncio.Task | None = None
    signaling_keepalive_task: asyncio.Task | None = None
    bye_event: asyncio.Event = field(default_factory=asyncio.Event)
    closing: bool = False


class SIPServerProtocol(asyncio.DatagramProtocol):
    """Netgsm trunk'ından gelen çağrıları doğrudan cevaplayan SIP UAS."""

    def __init__(self) -> None:
        self.settings = get_voice_settings()
        self.transport: asyncio.DatagramTransport | None = None
        self.active_calls: dict[str, SIPCall] = {}
        self.allowed_hosts = {
            item.strip()
            for item in self.settings.voice_sip_allowed_hosts.split(",")
            if item.strip()
        }

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport  # type: ignore[assignment]
        logger.info(
            "Doğrudan Netgsm SIP sunucusu hazır udp=%s:%s allowed=%s",
            self.settings.voice_server_host,
            self.settings.voice_server_port,
            ",".join(sorted(self.allowed_hosts)),
        )

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        if self.allowed_hosts and "*" not in self.allowed_hosts and addr[0] not in self.allowed_hosts:
            logger.warning("İzin verilmeyen SIP kaynağı source=%s", addr[0])
            return
        message = data.decode("utf-8", "replace")
        first_line = message.splitlines()[0] if message else ""
        if first_line.startswith("SIP/2.0"):
            self._handle_response(message)
            return
        method = first_line.split(" ", 1)[0].upper()
        if method == "INVITE":
            asyncio.create_task(self._handle_invite(message, addr))
        elif method == "ACK":
            logger.info("SIP ACK alındı call_id=%s", _header(message, "Call-ID"))
        elif method == "BYE":
            asyncio.create_task(self._handle_remote_bye(message, addr))
        elif method == "CANCEL":
            asyncio.create_task(self._handle_cancel(message, addr))
        elif method == "OPTIONS":
            self._send(self._response(message, "200 OK", extra="Allow: INVITE, ACK, CANCEL, BYE, OPTIONS\r\n"), addr)
        else:
            self._send(self._response(message, "405 Method Not Allowed", extra="Allow: INVITE, ACK, CANCEL, BYE, OPTIONS\r\n"), addr)

    def _handle_response(self, message: str) -> None:
        if not re.search(r"^SIP/2.0\s+2\d\d", message):
            return
        if not re.search(r"(?im)^CSeq:\s*\d+\s+BYE\s*$", message):
            return
        call = self.active_calls.get(_header(message, "Call-ID"))
        if call:
            logger.info("Netgsm SIP BYE onayı alındı call_id=%s", call.call_id)
            call.bye_event.set()

    async def _handle_invite(self, message: str, addr: tuple[str, int]) -> None:
        call_id = _header(message, "Call-ID")
        if not call_id:
            self._send(self._response(message, "400 Bad Request"), addr)
            return
        existing = self.active_calls.get(call_id)
        if existing:
            # UDP INVITE tekrar iletimi yeni bir konuşma oturumu açmamalı.
            self._send(existing.final_response, addr)
            return
        if len(self.active_calls) >= self.settings.voice_max_concurrent_calls:
            self._send(self._response(message, "486 Busy Here"), addr)
            return

        self._send(self._response(message, "100 Trying"), addr)
        media = self._parse_sdp(message, addr[0])
        if media is None:
            self._send(self._response(message, "488 Not Acceptable Here"), addr)
            return
        remote_ip, remote_port, dtmf_payload = media
        local_ip = self._local_ip_for(addr)
        local_tag = uuid.uuid4().hex[:16]
        call_uuid = str(uuid.uuid4())
        reader = asyncio.StreamReader(limit=1024 * 1024)

        async def terminate() -> None:
            await self.hangup(call_id)

        writer = DirectMediaWriter(terminate)
        loop = asyncio.get_running_loop()
        rtp_transport = None
        rtp_protocol = None
        local_rtp_port = self.settings.rtp_start_port
        while local_rtp_port <= self.settings.rtp_end_port:
            try:
                rtp_transport, rtp_protocol = await loop.create_datagram_endpoint(
                    lambda: RTPServerProtocol(
                        remote_ip,
                        remote_port,
                        lambda pcm: reader.feed_data(encode_frame(0x10, pcm)),
                        dtmf_payload_type=dtmf_payload,
                    ),
                    local_addr=(self.settings.voice_server_host, local_rtp_port),
                )
                break
            except OSError:
                local_rtp_port += 2
        if not rtp_transport or not rtp_protocol:
            self._send(self._response(message, "500 Server Internal Error"), addr)
            return
        writer.rtp = rtp_protocol

        to_value = _ensure_tag(_header(message, "To"), local_tag)
        media_ip = self.settings.voice_external_ip or local_ip
        response = self._response(
            message,
            "200 OK",
            to_value=to_value,
            extra=(
                f"Contact: <sip:{_request_uri_user(message) or 'voice'}@{local_ip}:{self.settings.voice_server_port}>\r\n"
                "Allow: INVITE, ACK, CANCEL, BYE, OPTIONS\r\n"
                "Supported: timer\r\n"
            ),
            body=self._sdp(media_ip, local_rtp_port, dtmf_payload),
        )
        call = SIPCall(
            call_id=call_id,
            call_uuid=call_uuid,
            invite=message,
            signaling_addr=addr,
            local_ip=local_ip,
            local_tag=local_tag,
            reader=reader,
            writer=writer,
            rtp_transport=rtp_transport,
            rtp_protocol=rtp_protocol,
            final_response=response,
        )
        self.active_calls[call_id] = call
        call.signaling_keepalive_task = asyncio.create_task(
            self._keep_signaling_alive(call_id)
        )

        caller = normalize_phone(_uri_user(_header(message, "From")))
        did = normalize_phone(
            _request_uri_user(message) or _uri_user(_header(message, "To"))
        )
        if not caller:
            caller = f"anonymous:{call_uuid[:12]}"
        await registry.put(CallContext(call_uuid, caller, did, call_id))
        reader.feed_data(encode_frame(0x01, uuid.UUID(call_uuid).bytes))
        # Doğrudan SIP/RTP taşımasını, alanları deterministik olarak biriktiren
        # ana DialogManager akışına bağla. Serbest VoiceLLMEngine rezervasyon
        # sahibi değildir ve müşteri söylemeden alan üretemez.
        call.task = asyncio.create_task(handle_audiosocket(reader, writer))
        call.task.add_done_callback(
            lambda _task, cid=call_id: asyncio.create_task(self._task_finished(cid))
        )
        self._send(self._response(message, "180 Ringing", to_value=to_value), addr)
        self._send(response, addr)
        logger.info(
            "Netgsm çağrısı doğrudan kabul edildi uuid=%s call_id=%s caller=%s did=%s rtp=%s:%s",
            call_uuid,
            call_id,
            redact_phone(caller),
            redact_phone(did),
            media_ip,
            local_rtp_port,
        )

    @staticmethod
    def _parse_sdp(message: str, fallback_ip: str) -> tuple[str, int, int] | None:
        connection = re.search(r"(?im)^c=IN\s+IP4\s+([^\s]+)", message)
        audio = re.search(r"(?im)^m=audio\s+(\d+)\s+RTP/AVP\s+(.+)$", message)
        if not audio:
            return None
        formats = audio.group(2).split()
        if "8" not in formats:
            return None
        dtmf = 101
        event = re.search(r"(?im)^a=rtpmap:(\d+)\s+telephone-event/8000", message)
        if event:
            dtmf = int(event.group(1))
        return (
            connection.group(1).strip() if connection else fallback_ip,
            int(audio.group(1)),
            dtmf,
        )

    async def _handle_remote_bye(self, message: str, addr: tuple[str, int]) -> None:
        self._send(self._response(message, "200 OK"), addr)
        call_id = _header(message, "Call-ID")
        call = self.active_calls.get(call_id)
        if call:
            logger.info("Netgsm çağrıyı kapattı call_id=%s", call_id)
            call.bye_event.set()
            await self._end_media(call_id)

    async def _handle_cancel(self, message: str, addr: tuple[str, int]) -> None:
        self._send(self._response(message, "200 OK"), addr)
        call_id = _header(message, "Call-ID")
        call = self.active_calls.get(call_id)
        if call:
            self._send(
                self._response(
                    call.invite,
                    "487 Request Terminated",
                    to_value=_ensure_tag(_header(call.invite, "To"), call.local_tag),
                ),
                call.signaling_addr,
            )
            await self._end_media(call_id)

    async def hangup(self, call_id: str) -> None:
        """Başarılı kapanış WAV'ından sonra Netgsm'e dialog-içi BYE gönderir."""
        call = self.active_calls.get(call_id)
        if not call or call.closing:
            return
        call.closing = True
        bye = self._build_bye(call)
        logger.info("Netgsm'e doğrudan SIP BYE gönderiliyor call_id=%s", call_id)
        for delay in (0.5, 1.0, 2.0):
            self._send(bye, call.signaling_addr)
            try:
                await asyncio.wait_for(call.bye_event.wait(), timeout=delay)
                break
            except TimeoutError:
                continue
        if not call.bye_event.is_set():
            logger.warning("Netgsm SIP BYE yanıt süresi doldu call_id=%s", call_id)
        await self._end_media(call_id)

    async def _end_media(self, call_id: str) -> None:
        call = self.active_calls.pop(call_id, None)
        if not call:
            return
        if (
            call.signaling_keepalive_task
            and call.signaling_keepalive_task is not asyncio.current_task()
        ):
            call.signaling_keepalive_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await call.signaling_keepalive_task
        call.writer._closed = True
        call.reader.feed_data(encode_frame(0x00))
        call.reader.feed_eof()
        call.rtp_transport.close()
        if call.task and call.task is not asyncio.current_task():
            with contextlib.suppress(asyncio.TimeoutError, asyncio.CancelledError):
                await asyncio.wait_for(asyncio.shield(call.task), timeout=3)
        await registry.remove(call.call_uuid)
        logger.info("Doğrudan SIP/RTP oturumu kapandı call_id=%s", call_id)

    async def _task_finished(self, call_id: str) -> None:
        call = self.active_calls.get(call_id)
        if call and not call.closing:
            # Konuşma çekirdeği beklenmedik biçimde döndüyse açık SIP kanalını bırakma.
            await self.hangup(call_id)

    async def _keep_signaling_alive(self, call_id: str) -> None:
        """Rölenin UDP eşlemesini uzun çağrılarda BYE'a kadar açık tutar."""
        while True:
            await asyncio.sleep(SIGNALING_KEEPALIVE_INTERVAL_SECONDS)
            call = self.active_calls.get(call_id)
            if not call or call.closing:
                return
            self._send(self._build_options_keepalive(call), call.signaling_addr)

    def _local_ip_for(self, addr: tuple[str, int]) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect(addr)
            return sock.getsockname()[0]
        except OSError:
            return "127.0.0.1"
        finally:
            sock.close()

    def _response(
        self,
        request: str,
        status: str,
        *,
        to_value: str | None = None,
        extra: str = "",
        body: str = "",
    ) -> str:
        vias = "".join(f"Via: {value}\r\n" for value in _header_values(request, "Via"))
        record_routes = "".join(
            f"Record-Route: {value}\r\n"
            for value in _header_values(request, "Record-Route")
        )
        content_headers = "Content-Type: application/sdp\r\n" if body else ""
        return (
            f"SIP/2.0 {status}\r\n"
            f"{vias}{record_routes}"
            f"From: {_header(request, 'From')}\r\n"
            f"To: {to_value if to_value is not None else _header(request, 'To')}\r\n"
            f"Call-ID: {_header(request, 'Call-ID')}\r\n"
            f"CSeq: {_header(request, 'CSeq')}\r\n"
            f"{extra}{content_headers}Content-Length: {len(body.encode())}\r\n\r\n{body}"
        )

    @staticmethod
    def _sdp(media_ip: str, rtp_port: int, dtmf_payload: int) -> str:
        session_id = random.randrange(1_000_000, 9_999_999)
        return (
            "v=0\r\n"
            f"o=- {session_id} {session_id} IN IP4 {media_ip}\r\n"
            "s=RandevumOnline\r\n"
            f"c=IN IP4 {media_ip}\r\n"
            "t=0 0\r\n"
            f"m=audio {rtp_port} RTP/AVP 8 {dtmf_payload}\r\n"
            "a=rtpmap:8 PCMA/8000\r\n"
            f"a=rtpmap:{dtmf_payload} telephone-event/8000\r\n"
            f"a=fmtp:{dtmf_payload} 0-16\r\n"
            "a=ptime:20\r\n"
            "a=sendrecv\r\n"
        )

    def _build_bye(self, call: SIPCall) -> str:
        remote_target = _contact_uri(call.invite)
        if not remote_target:
            remote_target = f"sip:{_uri_user(_header(call.invite, 'From'))}@{call.signaling_addr[0]}:{call.signaling_addr[1]}"
        routes = "".join(
            f"Route: {value}\r\n"
            for value in _header_values(call.invite, "Record-Route")
        )
        branch = f"z9hG4bK{uuid.uuid4().hex[:20]}"
        local_party = _ensure_tag(_header(call.invite, "To"), call.local_tag)
        remote_party = _header(call.invite, "From")
        return (
            f"BYE {remote_target} SIP/2.0\r\n"
            f"Via: SIP/2.0/UDP {call.local_ip}:{self.settings.voice_server_port};branch={branch};rport\r\n"
            "Max-Forwards: 70\r\n"
            f"{routes}From: {local_party}\r\n"
            f"To: {remote_party}\r\n"
            f"Call-ID: {call.call_id}\r\n"
            "CSeq: 1 BYE\r\n"
            f"Contact: <sip:voice@{call.local_ip}:{self.settings.voice_server_port}>\r\n"
            "User-Agent: RandevumOnline-Voice\r\n"
            "Content-Length: 0\r\n\r\n"
        )

    def _build_options_keepalive(self, call: SIPCall) -> str:
        """Ana dialog CSeq'inden bağımsız, geçerli bir SIP UDP keepalive üretir."""
        branch = f"z9hG4bK{uuid.uuid4().hex[:20]}"
        token = uuid.uuid4().hex
        target_host, target_port = call.signaling_addr
        return (
            f"OPTIONS sip:keepalive@{target_host}:{target_port} SIP/2.0\r\n"
            f"Via: SIP/2.0/UDP {call.local_ip}:{self.settings.voice_server_port};branch={branch};rport\r\n"
            "Max-Forwards: 70\r\n"
            f"From: <sip:voice@{call.local_ip}>;tag={token[:16]}\r\n"
            f"To: <sip:keepalive@{target_host}>\r\n"
            f"Call-ID: keepalive-{token}@{call.local_ip}\r\n"
            "CSeq: 1 OPTIONS\r\n"
            "User-Agent: RandevumOnline-Voice\r\n"
            "Content-Length: 0\r\n\r\n"
        )

    def _send(self, message: str, addr: tuple[str, int]) -> None:
        if self.transport and not self.transport.is_closing():
            self.transport.sendto(message.encode(), addr)

    async def close(self) -> None:
        for call_id in list(self.active_calls):
            await self.hangup(call_id)
        if self.transport:
            self.transport.close()


async def start_sip_server() -> tuple[asyncio.DatagramTransport, SIPServerProtocol]:
    settings = get_voice_settings()
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        SIPServerProtocol,
        local_addr=(settings.voice_server_host, settings.voice_server_port),
    )
    return transport, protocol
