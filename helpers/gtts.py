from gtts import gTTS

async def synthesize(text: str) -> bytes:
    """
    Synthesizes speech using Google's TTS in English (US).
    Returns MP3 bytes.
    """
    tts = gTTS(text=text, tld='us')
    return b"".join(tts.stream())
    