import asyncio
import pyttsx3

def _generate(text, output_path, voice_hint=None, rate=165):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    if voice_hint:
        hint = voice_hint.lower()
        for voice in engine.getProperty("voices"):
            blob = f"{voice.id} {voice.name}".lower()
            if hint in blob:
                engine.setProperty("voice", voice.id)
                break
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

async def generate_audio(text, output_path, voice="default"):
    await asyncio.to_thread(_generate, text, output_path, voice)
