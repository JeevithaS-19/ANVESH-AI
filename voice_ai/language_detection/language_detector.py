class LanguageDetector:
    LANGUAGE_MAP = {
        "en": "English",
        "hi": "Hindi",
        "kn": "Kannada",
        "ta": "Tamil",
        "te": "Telugu",
        "ml": "Malayalam",
        "mr": "Marathi",
        "bn": "Bengali",
        "gu": "Gujarati",
        "pa": "Punjabi",
        "ur": "Urdu",
        "or": "Odia"
    }

    def detect(self, language_code, confidence):
        language_name = self.LANGUAGE_MAP.get(
            language_code,
            "Unknown"
        )

        return {
            "language_code": language_code,
            "language": language_name,
            "confidence": confidence
        }


if __name__ == "__main__":
    detector = LanguageDetector()

    result = detector.detect("en", 0.6585)

    print("Language Code:", result["language_code"])
    print("Detected Language:", result["language"])
    print("Confidence:", result["confidence"])