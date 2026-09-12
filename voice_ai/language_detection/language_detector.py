class LanguageDetector:
    LANGUAGE_MAP = {
        "af": "Afrikaans",
        "ar": "Arabic",
        "bn": "Bengali",
        "bg": "Bulgarian",
        "ca": "Catalan",
        "cs": "Czech",
        "da": "Danish",
        "de": "German",
        "el": "Greek",
        "en": "English",
        "es": "Spanish",
        "et": "Estonian",
        "fa": "Persian",
        "fi": "Finnish",
        "fr": "French",
        "gu": "Gujarati",
        "he": "Hebrew",
        "hi": "Hindi",
        "hr": "Croatian",
        "hu": "Hungarian",
        "id": "Indonesian",
        "it": "Italian",
        "ja": "Japanese",
        "kn": "Kannada",
        "ko": "Korean",
        "lt": "Lithuanian",
        "lv": "Latvian",
        "ml": "Malayalam",
        "mr": "Marathi",
        "ne": "Nepali",
        "nl": "Dutch",
        "no": "Norwegian",
        "or": "Odia",
        "pa": "Punjabi",
        "pl": "Polish",
        "pt": "Portuguese",
        "ro": "Romanian",
        "ru": "Russian",
        "sk": "Slovak",
        "sl": "Slovenian",
        "sr": "Serbian",
        "sv": "Swedish",
        "sw": "Swahili",
        "ta": "Tamil",
        "te": "Telugu",
        "th": "Thai",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "vi": "Vietnamese",
        "zh": "Chinese"
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

    test_languages = [
        ("en", 0.95),
        ("hi", 0.91),
        ("kn", 0.89),
        ("ta", 0.92),
        ("te", 0.90),
        ("ml", 0.88)
    ]

    for language_code, confidence in test_languages:
        result = detector.detect(language_code, confidence)

        print(
            result["language_code"],
            "→",
            result["language"],
            "| Confidence:",
            result["confidence"]
        )