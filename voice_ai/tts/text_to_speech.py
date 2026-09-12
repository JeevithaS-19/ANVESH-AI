import pyttsx3


class TextToSpeech:

    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        if not text:
            return

        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":

    tts = TextToSpeech()

    message = "What is your highest level of education?"

    print("Speaking:")
    print(message)

    tts.speak(message)