import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.voice.tts import TextToSpeechEngine
from app.voice.config import get_voice_settings

async def main():
    print("Generating greeting audio...")
    tts = TextToSpeechEngine()
    text = "Merhaba. RandevumOnline yapay zeka asistanına hoş geldiniz. Size yardımcı olabilmem için lütfen randevu talebinizi söyleyebilirsiniz."
    
    # ensure assets dir exists
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "app", "voice", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    file_path = os.path.join(assets_dir, "greeting.alaw")
    
    # We call the synchronous _synthesize_pcm in a thread
    alaw_data = await asyncio.to_thread(tts._synthesize_pcm, text)
    
    with open(file_path, "wb") as f:
        f.write(alaw_data)
        
    print(f"Success! Audio saved to {file_path}")

if __name__ == "__main__":
    asyncio.run(main())
