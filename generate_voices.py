"""
Generate MP3 voice clips for the podium quotes using ElevenLabs TTS.
Reads API key + voice_id from M:\\MORRIS_OPS\\06_API_KEYS\\.
Outputs quote1.mp3 - quote4.mp3 next to index.html.
"""
import sys
import os
import urllib.request
import urllib.error
import json
from pathlib import Path

KEY_PATH   = Path(r"M:\MORRIS_OPS\06_API_KEYS\elevenlabs.txt")
VOICE_PATH = Path(r"M:\MORRIS_OPS\06_API_KEYS\elevenlabs_voice.txt")
OUT_DIR    = Path(__file__).parent
MODEL_ID   = "eleven_multilingual_v2"

QUOTES = [
    ("quote1.mp3",
     "I said to Melania. I said, Honey, there is a kid in the country. Jamieson. Rascal. Homeschooled. Deadlifts his bodyweight. Runs like the wind. She didn't believe me. Nobody believes me. But it's true. It's all true."),
    ("quote2.mp3",
     "Complex math. COMPLEX. Not easy math. Anybody can do easy math. Rascal does the complex stuff. One hundreds. Across the board. A plus. Beautiful to see."),
    ("quote3.mp3",
     "The dirt bike. You should see this kid on a dirt bike. Marksman too. A marksman! At his age! Unbelievable. The generals are calling me."),
    ("quote4.mp3",
     "And the Bible verses. Oh, the Bible verses. He recites the Armor of God. The WHOLE thing. I sat there. I listened. I said, Folks, this is the real deal."),
]

def read_trim(p: Path) -> str:
    return p.read_text(encoding="utf-8").strip()

def main():
    if not KEY_PATH.exists():
        sys.exit(f"Missing key file: {KEY_PATH}")
    if not VOICE_PATH.exists():
        sys.exit(f"Missing voice file: {VOICE_PATH}")

    api_key  = read_trim(KEY_PATH)
    voice_id = read_trim(VOICE_PATH)
    print(f"Voice ID: {voice_id}")
    print(f"Model:    {MODEL_ID}")
    print(f"Output:   {OUT_DIR}")
    print()

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    for filename, text in QUOTES:
        out = OUT_DIR / filename
        print(f"-> {filename}  ({len(text)} chars)")
        payload = json.dumps({
            "text": text,
            "model_id": MODEL_ID,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.85,
                "style": 0.35,
                "use_speaker_boost": True
            }
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            method="POST",
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                audio = resp.read()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            sys.exit(f"  FAILED ({e.code}): {body}")
        out.write_bytes(audio)
        print(f"  saved ({len(audio):,} bytes)")

    print("\nDone.")

if __name__ == "__main__":
    main()
