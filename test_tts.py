import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
from app.voice.tts import TextToSpeechEngine

async def test_tts():
    tts = TextToSpeechEngine()
    chunks = 0
    async for chunk in tts.synthesize_stream("Merhaba dünya"):
        chunks += 1
    print(f"Chunks generated: {chunks}")

asyncio.run(test_tts())
