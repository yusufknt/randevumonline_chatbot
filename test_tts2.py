import asyncio
from app.voice.tts import TextToSpeechEngine

async def test_tts():
    tts = TextToSpeechEngine()
    
    # We will mock the generator internally or just run it
    # We just want to see if the API actually sends bytes now
    # We'll just patch the payload in tts.py for a quick test
    pass

asyncio.run(test_tts())
