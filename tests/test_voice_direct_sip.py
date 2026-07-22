from __future__ import annotations

import struct
import unittest
from unittest.mock import AsyncMock, patch
from unittest.mock import Mock

from app.voice.rtp_server import RTPServerProtocol, alaw2lin, lin2alaw
from app.voice.sip_server import SIPCall, SIPServerProtocol


INVITE = """INVITE sip:08505555515@10.203.0.2:8010 SIP/2.0\r
Via: SIP/2.0/UDP 10.203.0.1:5060;branch=z9hG4bK-invite;rport\r
Record-Route: <sip:10.203.0.1;lr>\r
From: \"Müşteri\" <sip:+905321112233@netgsm>;tag=remote-tag\r
To: <sip:08505555515@randevumonline>\r
Call-ID: direct-call-1\r
CSeq: 42 INVITE\r
Contact: <sip:+905321112233@10.203.0.1:5060>\r
Content-Type: application/sdp\r
Content-Length: 180\r
\r
v=0\r
o=- 1 1 IN IP4 10.203.0.1\r
s=-\r
c=IN IP4 10.203.0.1\r
t=0 0\r
m=audio 12000 RTP/AVP 8 101\r
a=rtpmap:8 PCMA/8000\r
a=rtpmap:101 telephone-event/8000\r
"""


class FakeDatagramTransport:
    def __init__(self) -> None:
        self.sent: list[tuple[bytes, tuple[str, int]]] = []
        self.closed = False

    def sendto(self, data: bytes, addr: tuple[str, int]) -> None:
        self.sent.append((data, addr))

    def is_closing(self) -> bool:
        return self.closed

    def close(self) -> None:
        self.closed = True


class DirectSIPTests(unittest.IsolatedAsyncioTestCase):
    def test_pcma_codec_has_correct_silence_and_frame_size(self) -> None:
        pcm = struct.pack("<160h", *([0] * 160))
        encoded = lin2alaw(pcm)
        self.assertEqual(encoded, bytes([0xD5]) * 160)
        self.assertEqual(len(alaw2lin(encoded)), 320)

    def test_pcma_codec_accepts_full_pcm_range(self) -> None:
        samples = list(range(-32768, 32768, 257)) + [-7, -1, 0, 1, 7, 32767]
        pcm = b"".join(struct.pack("<h", value) for value in samples)
        encoded = lin2alaw(pcm)
        self.assertEqual(len(encoded), len(samples))
        self.assertEqual(len(alaw2lin(encoded)), len(pcm))

    def test_rtp_output_encodes_pcm_as_pcma(self) -> None:
        protocol = RTPServerProtocol("10.203.0.1", 12000, Mock())
        transport = FakeDatagramTransport()
        protocol.connection_made(transport)  # type: ignore[arg-type]
        protocol.send_pcm(struct.pack("<160h", *([0] * 160)))
        packet, addr = transport.sent[0]
        self.assertEqual(addr, ("10.203.0.1", 12000))
        self.assertEqual(packet[1] & 0x7F, 8)
        self.assertEqual(packet[12:], bytes([0xD5]) * 160)

    def test_rtp_playback_echo_is_not_forwarded_as_customer_speech(self) -> None:
        on_pcm = Mock()
        protocol = RTPServerProtocol("10.203.0.1", 12000, on_pcm)
        transport = FakeDatagramTransport()
        protocol.connection_made(transport)  # type: ignore[arg-type]
        samples = [int(8000 * ((index % 31) / 30 - 0.5)) for index in range(160)]
        pcm = struct.pack("<160h", *samples)
        protocol.send_pcm(pcm)
        protocol.send_pcm(pcm)
        echoed_packet = transport.sent[-1][0]
        protocol.datagram_received(echoed_packet, ("10.203.0.1", 12000))
        on_pcm.assert_not_called()

    def test_sdp_requires_pcma_and_reads_remote_media(self) -> None:
        self.assertEqual(
            SIPServerProtocol._parse_sdp(INVITE, "127.0.0.1"),
            ("10.203.0.1", 12000, 101),
        )
        self.assertIsNone(
            SIPServerProtocol._parse_sdp(
                INVITE.replace("RTP/AVP 8 101", "RTP/AVP 0 101"),
                "127.0.0.1",
            )
        )

    def test_bye_preserves_dialog_identity_and_route(self) -> None:
        server = SIPServerProtocol()
        reader = Mock()
        writer = Mock()
        call = SIPCall(
            call_id="direct-call-1",
            call_uuid="00000000-0000-0000-0000-000000000001",
            invite=INVITE,
            signaling_addr=("10.203.0.1", 5060),
            local_ip="10.203.0.2",
            local_tag="local-tag",
            reader=reader,
            writer=writer,
            rtp_transport=Mock(),
            rtp_protocol=Mock(),
            final_response="",
        )
        bye = server._build_bye(call)
        self.assertTrue(
            bye.startswith("BYE sip:+905321112233@10.203.0.1:5060 SIP/2.0")
        )
        self.assertIn("Route: <sip:10.203.0.1;lr>", bye)
        self.assertIn(
            "From: <sip:08505555515@randevumonline>;tag=local-tag", bye
        )
        self.assertIn(
            'To: "Müşteri" <sip:+905321112233@netgsm>;tag=remote-tag', bye
        )
        self.assertIn("Call-ID: direct-call-1", bye)
        self.assertIn("CSeq: 1 BYE", bye)

    def test_options_keepalive_is_separate_from_call_dialog(self) -> None:
        server = SIPServerProtocol()
        call = SIPCall(
            call_id="direct-call-1",
            call_uuid="00000000-0000-0000-0000-000000000001",
            invite=INVITE,
            signaling_addr=("10.203.0.1", 5060),
            local_ip="10.203.0.2",
            local_tag="local-tag",
            reader=Mock(),
            writer=Mock(),
            rtp_transport=Mock(),
            rtp_protocol=Mock(),
            final_response="",
        )

        keepalive = server._build_options_keepalive(call)

        self.assertTrue(
            keepalive.startswith("OPTIONS sip:keepalive@10.203.0.1:5060 SIP/2.0")
        )
        self.assertIn("CSeq: 1 OPTIONS", keepalive)
        self.assertIn("Call-ID: keepalive-", keepalive)
        self.assertNotIn("Call-ID: direct-call-1", keepalive)

    async def test_signaling_keepalive_uses_original_relay_address(self) -> None:
        server = SIPServerProtocol()
        call = SIPCall(
            call_id="direct-call-1",
            call_uuid="00000000-0000-0000-0000-000000000001",
            invite=INVITE,
            signaling_addr=("10.203.0.1", 5060),
            local_ip="10.203.0.2",
            local_tag="local-tag",
            reader=Mock(),
            writer=Mock(),
            rtp_transport=Mock(),
            rtp_protocol=Mock(),
            final_response="",
        )
        server.active_calls[call.call_id] = call
        sent: list[tuple[str, tuple[str, int]]] = []

        def capture(message: str, addr: tuple[str, int]) -> None:
            sent.append((message, addr))
            call.closing = True

        server._send = Mock(side_effect=capture)  # type: ignore[method-assign]
        with patch("app.voice.sip_server.asyncio.sleep", new=AsyncMock()) as sleep:
            await server._keep_signaling_alive(call.call_id)

        self.assertEqual(sent[0][1], call.signaling_addr)
        self.assertTrue(sent[0][0].startswith("OPTIONS "))
        sleep.assert_awaited()

    def test_incoming_bye_response_echoes_transaction_headers(self) -> None:
        server = SIPServerProtocol()
        bye = INVITE.replace(
            "INVITE sip:08505555515@10.203.0.2:8010",
            "BYE sip:08505555515@10.203.0.2:8010",
        ).replace("CSeq: 42 INVITE", "CSeq: 43 BYE")
        response = server._response(bye, "200 OK")
        self.assertIn("SIP/2.0 200 OK", response)
        self.assertIn("Call-ID: direct-call-1", response)
        self.assertIn("CSeq: 43 BYE", response)
        self.assertIn("Via: SIP/2.0/UDP 10.203.0.1:5060", response)


if __name__ == "__main__":
    unittest.main()
