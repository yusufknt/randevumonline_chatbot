import asyncio
from app.voice.tts import TextToSpeechEngine
async def main():
    e = TextToSpeechEngine()
    pcm = await asyncio.to_thread(e._synthesize_pcm, 'Merhaba')
    with open('test_output.alaw', 'wb') as f:
        f.write(pcm)
    print(f"File size: {len(pcm)} bytes")
asyncio.run(main())
