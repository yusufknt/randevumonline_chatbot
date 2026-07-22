"""
Sesli Randevu Botu (Voice Agent) Ana Sunucu Başlatıcı. (Asterisk'siz, Native Python)

Bu betik:
1. UDP 8010 portunda SIP INVITE isteklerini bekler.
2. 7/24 dinlemede kalarak gelen çağrıları eşzamanlı olarak işler ve RTP portları açar.
"""

import asyncio
import logging
from app.voice.sip_server import start_sip_server
from app.voice.config import get_voice_settings

# Log yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s"
)
logger = logging.getLogger(__name__)

async def main() -> None:
    settings = get_voice_settings()
    host = settings.voice_server_host
    port = settings.voice_server_port

    logger.info("SIP UDP Sunucusu başlatılıyor (%s:%s)...", host, port)
    transport, protocol = await start_sip_server()

    try:
        # 7/24 çalışmasını sağla
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("SIP Sunucusu kapatılıyor...")
    finally:
        await protocol.close()
        logger.info("Sunucu başarıyla kapatıldı.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Kullanıcı tarafından durduruldu.")
