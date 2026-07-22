"""Netgsm ile doğrudan PCMA/RTP medya taşıyıcısı."""

from __future__ import annotations

import asyncio
import logging
import random
import struct
import time
from collections import deque
from collections.abc import Callable

import numpy as np

logger = logging.getLogger(__name__)


# ITU-T G.711 A-law dönüşüm tablosu. Telefon tarafından gelen PCMA, mevcut
# DialogManager hattının beklediği 8 kHz mono signed-linear PCM'e çevrilir.
ALAW_DECODE_TABLE = [0] * 256
for _index in range(256):
    _alaw = _index ^ 0x55
    _exponent = (_alaw & 0x70) >> 4
    _sample = ((_alaw & 0x0F) << 4) + 8
    if _exponent:
        _sample = (_sample + 0x100) << (_exponent - 1)
    ALAW_DECODE_TABLE[_index] = _sample if _alaw & 0x80 else -_sample


def alaw2lin(data: bytes) -> bytes:
    """PCMA/A-law baytlarını little-endian signed 16-bit PCM'e çevirir."""
    output = bytearray(len(data) * 2)
    for index, value in enumerate(data):
        struct.pack_into("<h", output, index * 2, ALAW_DECODE_TABLE[value])
    return bytes(output)


def _linear_sample_to_alaw(sample: int) -> int:
    # Sun/ITU G.711 referans algoritması. A-law işaret biti pozitif örneklerde
    # set edilir; son adımda çift bitler 0x55 ile terslenir.
    mask = 0xD5
    if sample < 0:
        mask = 0x55
        # -1..-7 aralığında bias sonrası negatif değer üretmek bytes()
        # dönüşümünü kırıyordu. G.711 giriş büyüklüğü sıfırın altına inemez.
        sample = max(0, -sample - 8)
    sample = min(sample, 32635)
    if sample < 256:
        encoded = sample >> 4
    else:
        exponent = max(1, sample.bit_length() - 8)
        encoded = (exponent << 4) | ((sample >> (exponent + 3)) & 0x0F)
    return encoded ^ mask


def lin2alaw(data: bytes) -> bytes:
    """Little-endian signed 16-bit PCM'i PCMA/A-law'a çevirir."""
    usable = len(data) - (len(data) % 2)
    return bytes(
        _linear_sample_to_alaw(sample[0])
        for sample in struct.iter_unpack("<h", data[:usable])
    )


class RTPServerProtocol(asyncio.DatagramProtocol):
    """Tek SIP diyaloğunun simetrik RTP akışını taşır.

    ``on_pcm`` AudioSocket tabanlı çalışan konuşma çekirdeğine 20 ms PCM
    kareleri verir. Çıkışta çekirdeğin PCM'i mutlaka PCMA'ya kodlanır.
    """

    def __init__(
        self,
        remote_ip: str,
        remote_port: int,
        on_pcm: Callable[[bytes], None],
        payload_type: int = 8,
        dtmf_payload_type: int = 101,
    ) -> None:
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.on_pcm = on_pcm
        self.payload_type = payload_type
        self.dtmf_payload_type = dtmf_payload_type
        self.transport: asyncio.DatagramTransport | None = None
        self.sequence_number = random.randrange(0x10000)
        self.timestamp = random.randrange(0x100000000)
        self.ssrc = random.randrange(1, 0x100000000)
        self._outbound_audio: deque[tuple[float, np.ndarray]] = deque()
        self._echo_suppressed = 0

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport  # type: ignore[assignment]
        logger.info(
            "Doğrudan RTP hazır remote=%s:%s codec=PCMA/8000",
            self.remote_ip,
            self.remote_port,
        )

    @staticmethod
    def _payload(data: bytes) -> tuple[int, bytes] | None:
        if len(data) < 12 or data[0] >> 6 != 2:
            return None
        csrc_count = data[0] & 0x0F
        offset = 12 + (csrc_count * 4)
        if len(data) < offset:
            return None
        if data[0] & 0x10:
            if len(data) < offset + 4:
                return None
            extension_words = struct.unpack_from("!H", data, offset + 2)[0]
            offset += 4 + extension_words * 4
            if len(data) < offset:
                return None
        payload = data[offset:]
        if data[0] & 0x20:
            if not payload or payload[-1] > len(payload):
                return None
            payload = payload[:-payload[-1]]
        return data[1] & 0x7F, payload

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        parsed = self._payload(data)
        if not parsed:
            return
        payload_type, payload = parsed
        if payload_type != self.payload_type or not payload:
            return
        # Netgsm/Asterisk'teki rtp_symmetric davranışını koru: ilk gerçek medya
        # paketinin kaynak adresi SDP'den farklıysa cevapları oraya gönder.
        if (self.remote_ip, self.remote_port) != addr:
            self.remote_ip, self.remote_port = addr
            logger.info("Simetrik RTP hedefi güncellendi remote=%s:%s", *addr)
        pcm = alaw2lin(payload)
        if self._is_playback_echo(pcm):
            self._echo_suppressed += 1
            if self._echo_suppressed == 1 or self._echo_suppressed % 50 == 0:
                logger.info(
                    "RTP oynatma yankısı bastırıldı frames=%d",
                    self._echo_suppressed,
                )
            return
        self.on_pcm(pcm)

    def _is_playback_echo(self, pcm_data: bytes) -> bool:
        """Yakın zamanda gönderilen sesin hat üzerinden dönen kopyasını ayıklar.

        Kullanıcının eşzamanlı konuşması yankıyla aynı dalga biçimine sahip
        olmadığından korelasyonu düşürür ve barge-in olarak iletilmeye devam eder.
        """
        from app.voice.config import get_voice_settings

        cfg = get_voice_settings()
        now = time.monotonic()
        window_s = max(0.2, cfg.voice_rtp_echo_window_ms / 1000.0)
        while self._outbound_audio and now - self._outbound_audio[0][0] > window_s:
            self._outbound_audio.popleft()
        if len(self._outbound_audio) < 2:
            return False
        incoming = np.frombuffer(pcm_data, dtype="<i2").astype(np.float32)[::4]
        incoming -= float(incoming.mean())
        incoming_norm = float(np.linalg.norm(incoming))
        if incoming_norm < 250.0:
            return False
        frames = list(self._outbound_audio)
        threshold = cfg.voice_rtp_echo_correlation
        # RTP saatlerinin fazı farklı olabilir. Komşu iki 20 ms kare içinde
        # 2.5 ms adımlarla kaydırarak karşılaştır.
        for index in range(len(frames) - 1):
            candidate = np.concatenate((frames[index][1], frames[index + 1][1]))
            for offset in range(0, len(frames[index][1]) + 1, 10):
                part = candidate[offset:offset + len(incoming)].copy()
                if len(part) != len(incoming):
                    continue
                part -= float(part.mean())
                denominator = incoming_norm * float(np.linalg.norm(part))
                if denominator and abs(float(np.dot(incoming, part)) / denominator) >= threshold:
                    return True
        return False

    def send_pcm(self, pcm_data: bytes) -> None:
        if not self.transport or self.transport.is_closing() or not pcm_data:
            return
        alaw_data = lin2alaw(pcm_data)
        played_pcm = alaw2lin(alaw_data)
        played = np.frombuffer(played_pcm, dtype="<i2").astype(np.float32)[::4]
        self._outbound_audio.append((time.monotonic(), played))
        header = struct.pack(
            "!BBHII",
            0x80,
            self.payload_type,
            self.sequence_number,
            self.timestamp,
            self.ssrc,
        )
        self.transport.sendto(
            header + alaw_data, (self.remote_ip, self.remote_port)
        )
        self.sequence_number = (self.sequence_number + 1) & 0xFFFF
        self.timestamp = (self.timestamp + len(alaw_data)) & 0xFFFFFFFF

    def error_received(self, exc: Exception) -> None:
        logger.warning("RTP UDP hatası type=%s", type(exc).__name__)
