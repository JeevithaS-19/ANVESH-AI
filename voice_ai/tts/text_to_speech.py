import asyncio
import os
import uuid

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

    def generate_audio(self, text, language_code="en"):
        """
        Generate an MP3 file without playing it.

        Each generated audio file receives a unique filename
        so different conversations do not overwrite each other.
        """

        if not text:
            return {
                "success": False,
                "language": language_code,
                "message": "No text provided"
            }

        # Select voice for requested language
        voice = self.VOICES.get(language_code)

        # Fallback to English for unsupported languages
        if voice is None:
            voice = self.VOICES["en"]
            used_language = "en"
            fallback = True
        else:
            used_language = language_code
            fallback = False

        try:
            # Directory for generated audio files
            audio_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "generated_audio"
            )

            os.makedirs(audio_dir, exist_ok=True)

            # Create a unique filename
            unique_id = uuid.uuid4().hex[:8]

            output_file = os.path.join(
                audio_dir,
                f"tts_{language_code}_{unique_id}.mp3"
            )

            # Generate speech
            asyncio.run(
                self._generate_audio(
                    text,
                    voice,
                    output_file
                )
            )

            return {
                "success": True,
                "requested_language": language_code,
                "used_language": used_language,
                "voice": voice,
                "fallback": fallback,
                "audio_file": output_file
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

    def speak(self, text, language_code="en"):
        """
        Generate and play speech locally.

        The generated file is deleted after playback.
        """

        result = self.generate_audio(
            text,
            language_code
        )

        if not result["success"]:
            return result

        output_file = result["audio_file"]

        try:
            # Play generated speech
            playsound(output_file)

            # Delete temporary playback file
            if os.path.exists(output_file):
                os.remove(output_file)

            result.pop("audio_file", None)

            return result

        except Exception as e:

            if os.path.exists(output_file):
                os.remove(output_file)

            return {
                "success": False,
                "requested_language": language_code,
                "used_language": result["used_language"],
                "voice": result["voice"],
                "fallback": result["fallback"],
                "message": str(e)
            }


if __name__ == "__main__":

    tts = TextToSpeech()

    print("\n--- English TTS ---")
    print(
        tts.speak(
            "May I know your name?",
            "en"
        )
    )

    print("\n--- Hindi TTS ---")
    print(
        tts.speak(
            "आपका नाम क्या है?",
            "hi"
        )
    )

    print("\n--- Kannada TTS ---")
    print(
        tts.speak(
            "ನಿಮ್ಮ ಹೆಸರು ಏನು?",
            "kn"
        )
    )

    print("\n--- Audio File Generation Test ---")

    result = tts.generate_audio(
        "Your profile is ready.",
        "en"
    )

    print(result)