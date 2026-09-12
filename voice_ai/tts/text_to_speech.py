import pyttsx3


class TextToSpeech:

    LANGUAGE_VOICES = {
        "en": "en-US",
        "en-US": "en-US",
        "en-GB": "en-GB"
    }

    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")

    def find_voice(self, language_code):

        target_language = self.LANGUAGE_VOICES.get(
            language_code,
            language_code
        )

        for voice in self.voices:

            for language in voice.languages:

                if target_language.lower() in str(language).lower():
                    return voice

        return None

    def speak(self, text, language_code="en"):

        if not text:
            return {
                "success": False,
                "language": language_code,
                "message": "No text provided"
            }

        voice = self.find_voice(language_code)

        if voice is None:

            voice = self.find_voice("en")

            if voice is None:
                return {
                    "success": False,
                    "language": language_code,
                    "message": "No suitable TTS voice available"
                }

            used_language = "en"
            fallback = True

        else:

            used_language = language_code
            fallback = False

        self.engine.setProperty("voice", voice.id)

        self.engine.say(text)
        self.engine.runAndWait()

        return {
            "success": True,
            "requested_language": language_code,
            "used_language": used_language,
            "fallback": fallback
        }


if __name__ == "__main__":

    tts = TextToSpeech()

    result = tts.speak(
        "What is your highest level of education?",
        "en"
    )

    print(result)