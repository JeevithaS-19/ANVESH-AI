import asyncio
import os
import threading
import uuid

import edge_tts


# ============================================================
# VOICES
# ============================================================

VOICES = {

    "en": "en-IN-NeerjaNeural",

    "hi": "hi-IN-SwaraNeural",

    "kn": "kn-IN-SapnaNeural",
}


# ============================================================
# TEXT TO SPEECH
# ============================================================

class TextToSpeech:

    def __init__(self):

        self.output_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "..",
            "generated_audio"
        )

        self.output_dir = os.path.abspath(
            self.output_dir
        )

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    # ========================================================
    # ASYNC GENERATION
    # ========================================================

    async def _generate_audio(
        self,
        text,
        language
    ):

        if language not in VOICES:

            language = "en"

        voice = VOICES[
            language
        ]

        filename = (
            f"tts_{language}_"
            f"{uuid.uuid4().hex[:8]}"
            ".mp3"
        )

        output_file = os.path.join(
            self.output_dir,
            filename
        )

        communicate = edge_tts.Communicate(
            text,
            voice
        )

        await communicate.save(
            output_file
        )

        return {
            "success": True,

            "requested_language":
                language,

            "used_language":
                language,

            "voice":
                voice,

            "fallback":
                False,

            "audio_file":
                output_file,
        }

    # ========================================================
    # RUN COROUTINE SAFELY
    # ========================================================

    def _run_async_safely(
        self,
        coroutine
    ):

        result = {
            "value": None,
            "error": None,
        }

        def runner():

            try:

                result["value"] = (
                    asyncio.run(
                        coroutine
                    )
                )

            except Exception as error:

                result["error"] = error

        thread = threading.Thread(
            target=runner
        )

        thread.start()

        thread.join()

        if result["error"]:

            raise result["error"]

        return result["value"]

    # ========================================================
    # GENERATE AUDIO
    # ========================================================

    def generate_audio(
        self,
        text,
        language="en"
    ):

        if not text:
            return {
                "success": False,
                "error": "Empty text"
            }

        try:

            return self._run_async_safely(
                self._generate_audio(
                    text,
                    language
                )
            )

        except Exception as error:

            return {
                "success": False,
                "error": str(error),
            }

    # ========================================================
    # PLAY AUDIO
    # ========================================================

    def play_audio(
        self,
        audio_file
    ):

        try:

            from playsound import playsound

            playsound(
                audio_file
            )

            return True

        except Exception as error:

            print(
                "[TTS] Playback error:",
                error
            )

            return False

    # ========================================================
    # SPEAK
    # ========================================================

    def speak(
        self,
        text,
        language="en"
    ):

        result = (
            self.generate_audio(
                text,
                language
            )
        )

        if not result.get(
            "success"
        ):

            return result

        audio_file = result.get(
            "audio_file"
        )

        if audio_file:

            self.play_audio(
                audio_file
            )

            try:

                os.remove(
                    audio_file
                )

            except Exception:
                pass

        return result