import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.voice.tts import TextToSpeechEngine

async def main():
    print("Generating new greeting...")
    tts = TextToSpeechEngine()
    text = "Merhaba. RandevumOnline yapay zeka asistanına hoş geldiniz. Size yardımcı olabilmem için lütfen randevu talebinizi söyleyebilirsiniz."
    
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "app", "voice", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    file_path = os.path.join(assets_dir, "greeting.alaw")
    
    alaw_data = await asyncio.to_thread(tts._synthesize_pcm, text)
    
    with open(file_path, "wb") as f:
        f.write(alaw_data)
        
    print(f"DONE: {file_path}")

if __name__ == "__main__":
    asyncio.run(main())
