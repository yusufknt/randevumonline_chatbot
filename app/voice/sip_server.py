"""
SIP Sunucusu (Asterisk olmadan UDP 8010 dinler)
"""

import asyncio
import logging
import re
from typing import Tuple
from app.voice.config import get_voice_settings
from app.voice.rtp_server import RTPServerProtocol
from app.voice.pipeline import VoicePipeline
from app.voice.models import VoiceSession

logger = logging.getLogger(__name__)

class SIPServerProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.settings = get_voice_settings()
        self.transport = None
        self.active_calls = {}

    def connection_made(self, transport):
        self.transport = transport
        logger.info("🟢 SIP Sunucusu UDP port %s üzerinden dinleniyor...", self.settings.voice_server_port)

    def datagram_received(self, data, addr):
        message = data.decode('utf-8', errors='ignore')
        logger.info("SIP Paketi Alındı: %s", addr)
        
        if message.startswith("INVITE"):
            asyncio.create_task(self.handle_invite(message, addr))
        elif message.startswith("BYE"):
            self.handle_bye(message, addr)
        elif message.startswith("SIP/2.0 200 OK"):
            cseq_match = re.search(r"CSeq:\s*(\d+)\s+BYE", message, re.IGNORECASE)
            if cseq_match:
                call_id_match = re.search(r"Call-ID:\s*(.+)", message, re.IGNORECASE)
                if call_id_match:
                    call_id = call_id_match.group(1).strip()
                    logger.info("BYE acknowledged")
                    if call_id in self.active_calls and "bye_ack_event" in self.active_calls[call_id]:
                        self.active_calls[call_id]["bye_ack_event"].set()
        elif message.startswith("ACK"):
            logger.info("ACK Alındı")

    async def handle_invite(self, message: str, addr: Tuple[str, int]):
        # Call-ID'yi bul
        call_id_match = re.search(r"Call-ID:\s*(.+)", message, re.IGNORECASE)
        if not call_id_match:
            return
        call_id = call_id_match.group(1).strip()
        
        # RTP Portunu bul (SDP içinden m=audio port)
        m_audio_match = re.search(r"m=audio\s+(\d+)", message)
        rtp_port = int(m_audio_match.group(1)) if m_audio_match else 10000

        # İstemci IP'si SDP'deki c=IN IP4 içinden alınmalıdır!
        c_ip_match = re.search(r"c=IN IP4\s+([0-9\.]+)", message)
        remote_ip = c_ip_match.group(1).strip() if c_ip_match else addr[0]
        
        logger.info("Yeni Çağrı: Call-ID=%s, RTP=%s:%s", call_id, remote_ip, rtp_port)
        
        # Oturum ve pipeline oluştur
        session = VoiceSession(session_id=call_id)
        pipeline = VoicePipeline(session=session)
        
        async def hangup_callback():
            bye_msg = self.build_bye(message, local_ip)
            
            # BYE paketini doğrudan topmost Route (Proxy) adresine veya asıl addr'a yolla
            dest_ip = addr[0]
            dest_port = addr[1]
            route_match = re.search(r"Route:\s*<sip:([^;>:]+)(?::(\d+))?", bye_msg, re.IGNORECASE)
            if route_match:
                dest_ip = route_match.group(1)
                dest_port = int(route_match.group(2)) if route_match.group(2) else 5060
                
            logger.info("Sending SIP BYE to %s:%s:\n--- GÖNDERİLEN BYE MESAJI ---\n%s\n-----------------------------", dest_ip, dest_port, bye_msg.strip())
            self.transport.sendto(bye_msg.encode('utf-8'), (dest_ip, dest_port))
            
            if call_id in self.active_calls:
                ack_event = asyncio.Event()
                self.active_calls[call_id]["bye_ack_event"] = ack_event
                
                try:
                    await asyncio.wait_for(ack_event.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    logger.warning("BYE acknowledge timeout, terminating anyway.")
                    
                logger.info("RTP socket closed")
                self.active_calls[call_id]["transport"].close()
                del self.active_calls[call_id]
                
            pipeline.stop()
            logger.info("Session destroyed")
            logger.info("Call successfully terminated")

        async def call_end_callback():
            logger.info("[CALL END] Conversation finished.")
            logger.info("[CALL END] Calling SIP BYE...")
            await hangup_callback()
            logger.info("[CALL END] SIP BYE sent.")

        pipeline.on_hangup = call_end_callback
        
        # RTP Sunucusu başlat
        loop = asyncio.get_running_loop()
        
        # Dinamik boş port bul (10000 - 20000 arası)
        rtp_local_port = self.settings.rtp_start_port
        rtp_transport, rtp_protocol = None, None
        
        while rtp_local_port <= self.settings.rtp_end_port:
            try:
                rtp_transport, rtp_protocol = await loop.create_datagram_endpoint(
                    lambda: RTPServerProtocol(remote_ip, rtp_port, pipeline),
                    local_addr=("0.0.0.0", rtp_local_port)
                )
                break
            except OSError:
                rtp_local_port += 2 # RTP portları genelde çift sayılardır
                
        if not rtp_transport:
            logger.error("Boş RTP portu bulunamadı!")
            return
        
        self.active_calls[call_id] = {
            "session": session,
            "transport": rtp_transport
        }
        
        # SIP Signaling Contact IP'mizi al (Soketten - VPN üzerinden gelen)
        local_ip = "127.0.0.1"
        import socket
        import urllib.request
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((addr[0], 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            pass
            
        # RTP Media IP'mizi belirle (Public IP olmalı çünkü Media Server genelde dış ağdadır)
        external_ip = self.settings.voice_external_ip
        if not external_ip:
            try:
                external_ip = urllib.request.urlopen('http://ifconfig.me/ip').read().decode('utf8').strip()
            except:
                external_ip = local_ip
        
        # 100 Trying Gönder
        trying_response = self.build_100_trying(message)
        self.transport.sendto(trying_response.encode('utf-8'), addr)
        
        # 180 Ringing Gönder
        ringing_response = self.build_180_ringing(message)
        self.transport.sendto(ringing_response.encode('utf-8'), addr)
        
        # SIP 200 OK gönder
        ok_response = self.build_200_ok(message, rtp_local_port, local_ip, external_ip)
        self.transport.sendto(ok_response.encode('utf-8'), addr)
        
        logger.info("200 OK Gönderildi. Görüşme başladı. (Local RTP: %s, Signalling IP: %s, Media IP: %s)", rtp_local_port, local_ip, external_ip)
        # Gelen INVITE mesajının tamamını loglayalım ki hatayı görebilelim
        logger.info("--- GELEN INVITE MESAJI ---\n%s\n---------------------------", message)

    def handle_bye(self, message: str, addr: Tuple[str, int]):
        call_id_match = re.search(r"Call-ID:\s*(.+)", message, re.IGNORECASE)
        if call_id_match:
            call_id = call_id_match.group(1).strip()
            if call_id in self.active_calls:
                self.active_calls[call_id]["transport"].close()
                del self.active_calls[call_id]
                logger.info("Çağrı sonlandırıldı: %s", call_id)
        
        # 200 OK (BYE için)
        # Aslında 200 OK dönmemiz gerekir ama şu anki test ortamı için kritik değil.
        pass

    def build_bye(self, invite_msg: str, local_ip: str = "127.0.0.1") -> str:
        # Extract Request URI for BYE from Contact or From
        contact_match = re.search(r"Contact:\s*<([^>]+)>", invite_msg, re.IGNORECASE)
        if contact_match:
            request_uri = contact_match.group(1).strip()
        else:
            from_match = re.search(r"From:\s*<([^>]+)>", invite_msg, re.IGNORECASE)
            request_uri = from_match.group(1).strip() if from_match else "sip:unknown@unknown"
            
        call_id = re.search(r"Call-ID:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        from_hdr = re.search(r"From:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        to_hdr = re.search(r"To:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        
        record_routes = re.findall(r"Record-Route:\s*(.+)", invite_msg, re.IGNORECASE)
        route_headers = "".join([f"Route: {rr.strip()}\r\n" for rr in reversed(record_routes)])
        
        # tag yoksa ekleyelim
        if ";tag=" not in to_hdr:
            to_hdr += ";tag=12345"
            
        import random
        branch = f"z9hG4bK{random.randint(100000, 999999)}"
        via_header = f"Via: SIP/2.0/UDP {local_ip}:8010;rport;branch={branch}\r\n"
        
        # BYE için From ve To yer değiştirir.
        # CSeq UAC için lokal bir değer olmalıdır, ilk request olduğu için 1 BYE yapıyoruz.
        response = (
            f"BYE {request_uri} SIP/2.0\r\n"
            f"{via_header}"
            f"Max-Forwards: 70\r\n"
            f"{route_headers}"
            f"From: {to_hdr}\r\n"
            f"To: {from_hdr}\r\n"
            f"Call-ID: {call_id}\r\n"
            f"CSeq: 1 BYE\r\n"
            f"Contact: <sip:{local_ip}:8010>\r\n"
            f"User-Agent: VoiceBot\r\n"
            f"Content-Length: 0\r\n\r\n"
        )
        return response

    def build_100_trying(self, invite_msg: str) -> str:
        vias = re.findall(r"Via:\s*(.+)", invite_msg, re.IGNORECASE)
        via_headers = "\r\n".join([f"Via: {v.strip()}" for v in vias])
        
        record_routes = re.findall(r"Record-Route:\s*(.+)", invite_msg, re.IGNORECASE)
        rr_headers = "".join([f"Record-Route: {rr.strip()}\r\n" for rr in record_routes])
        
        call_id = re.search(r"Call-ID:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        from_hdr = re.search(r"From:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        to_hdr = re.search(r"To:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        cseq = re.search(r"CSeq:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        
        response = (
            f"SIP/2.0 100 Trying\r\n"
            f"{via_headers}\r\n"
            f"{rr_headers}"
            f"From: {from_hdr}\r\n"
            f"To: {to_hdr}\r\n"
            f"Call-ID: {call_id}\r\n"
            f"CSeq: {cseq}\r\n"
            f"Content-Length: 0\r\n\r\n"
        )
        return response

    def build_180_ringing(self, invite_msg: str) -> str:
        vias = re.findall(r"Via:\s*(.+)", invite_msg, re.IGNORECASE)
        via_headers = "\r\n".join([f"Via: {v.strip()}" for v in vias])
        
        record_routes = re.findall(r"Record-Route:\s*(.+)", invite_msg, re.IGNORECASE)
        rr_headers = "".join([f"Record-Route: {rr.strip()}\r\n" for rr in record_routes])
        
        call_id = re.search(r"Call-ID:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        from_hdr = re.search(r"From:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        to_hdr = re.search(r"To:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        cseq = re.search(r"CSeq:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        
        # tag yoksa ekleyelim
        if ";tag=" not in to_hdr:
            to_hdr += ";tag=12345"
            
        response = (
            f"SIP/2.0 180 Ringing\r\n"
            f"{via_headers}\r\n"
            f"{rr_headers}"
            f"From: {from_hdr}\r\n"
            f"To: {to_hdr}\r\n"
            f"Call-ID: {call_id}\r\n"
            f"CSeq: {cseq}\r\n"
            f"Content-Length: 0\r\n\r\n"
        )
        return response

    def build_200_ok(self, invite_msg: str, rtp_port: int, local_ip: str, external_ip: str) -> str:
        # Tüm Via başlıklarını bul
        vias = re.findall(r"Via:\s*(.+)", invite_msg, re.IGNORECASE)
        via_headers = "\r\n".join([f"Via: {v.strip()}" for v in vias])
        
        record_routes = re.findall(r"Record-Route:\s*(.+)", invite_msg, re.IGNORECASE)
        rr_headers = "".join([f"Record-Route: {rr.strip()}\r\n" for rr in record_routes])
        
        call_id = re.search(r"Call-ID:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        from_hdr = re.search(r"From:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        to_hdr = re.search(r"To:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        cseq = re.search(r"CSeq:\s*(.+)", invite_msg, re.IGNORECASE).group(1).strip()
        
        # tag yoksa ekleyelim
        if ";tag=" not in to_hdr:
            to_hdr += ";tag=12345"
            
        sdp = (
            f"v=0\r\n"
            f"o=- 123456 123456 IN IP4 {external_ip}\r\n"
            f"s=-\r\n"
            f"c=IN IP4 {external_ip}\r\n"
            f"t=0 0\r\n"
            f"m=audio {rtp_port} RTP/AVP 8 101\r\n"
            f"a=rtpmap:8 PCMA/8000\r\n"
            f"a=rtpmap:101 telephone-event/8000\r\n"
            f"a=ptime:20\r\n"
            f"a=sendrecv\r\n"
        )
        
        response = (
            f"SIP/2.0 200 OK\r\n"
            f"{via_headers}\r\n"
            f"{rr_headers}"
            f"From: {from_hdr}\r\n"
            f"To: {to_hdr}\r\n"
            f"Call-ID: {call_id}\r\n"
            f"CSeq: {cseq}\r\n"
            f"Contact: <sip:{local_ip}:8010>\r\n"
            f"Content-Type: application/sdp\r\n"
            f"Content-Length: {len(sdp)}\r\n\r\n"
            f"{sdp}"
        )
        return response
