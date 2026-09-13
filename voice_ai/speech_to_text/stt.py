from faster_whisper import WhisperModel


class SpeechToText:
    def __init__(self, model_size="base"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_file):
        segments, info = self.model.transcribe(audio_file)

        text = " ".join(segment.text.strip() for segment in segments)

        return {
            "text": text,
            "language": info.language,
            "language_probability": info.language_probability
        }


if __name__ == "__main__":
    stt = SpeechToText()

    result = stt.transcribe("sample.m4a")

    print("Detected Language:", result["language"])
    print("Confidence:", result["language_probability"])
    print("Transcription:", result["text"])