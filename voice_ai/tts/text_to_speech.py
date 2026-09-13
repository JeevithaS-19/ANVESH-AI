import asyncio
import os
import tempfile

import edge_tts
import pyttsx3
from playsound3 import playsound


class TextToSpeech:

    VOICES = {
        "en": "en-IN-NeerjaNeural",
        "hi": "hi-IN-SwaraNeural",
        "kn": "kn-IN-SapnaNeural"
    }

    def __init__(self):
        # Keep pyttsx3 for offline English fallback
        self.engine = pyttsx3.init()

    async def _generate_audio(self, text, voice, output_file):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    def speak(self, text, language_code="en"):

        if not text:
            return {
                "success": False,
                "language": language_code,
                "message": "No text provided"
            }

        # Use English as fallback for unsupported languages
        voice = self.VOICES.get(language_code)

        if voice is None:
            voice = self.VOICES["en"]
            used_language = "en"
            fallback = True
        else:
            used_language = language_code
            fallback = False

        try:
            # Temporary MP3 file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            )
            temp_file.close()

            output_file = temp_file.name

            # Generate speech
            asyncio.run(
                self._generate_audio(
                    text,
                    voice,
                    output_file
                )
            )

            # Play speech
            playsound(output_file)

            # Remove temporary file
            if os.path.exists(output_file):
                os.remove(output_file)

            return {
                "success": True,
                "requested_language": language_code,
                "used_language": used_language,
                "voice": voice,
                "fallback": fallback
            }

        except Exception as e:

            return {
                "success": False,
                "requested_language": language_code,
                "used_language": used_language,
                "voice": voice,
                "fallback": fallback,
                "message": str(e)
            }


if __name__ == "__main__":

    tts = TextToSpeech()

    print("\n--- English TTS ---")
    print(tts.speak(
        "May I know your name?",
        "en"
    ))

    print("\n--- Hindi TTS ---")
    print(tts.speak(
        "आपका नाम क्या है?",
        "hi"
    ))

    print("\n--- Kannada TTS ---")
    print(tts.speak(
        "ನಿಮ್ಮ ಹೆಸರು ಏನು?",
        "kn"
    ))