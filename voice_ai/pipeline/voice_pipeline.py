from voice_ai.speech_to_text.stt import SpeechToText
from voice_ai.language_detection.language_detector import LanguageDetector
from voice_ai.nlp.nlp_processor import NLPProcessor
from voice_ai.entity_extraction.entity_extractor import EntityExtractor
from voice_ai.conversation.conversation_manager import ConversationManager
from voice_ai.tts.text_to_speech import TextToSpeech


class VoicePipeline:

    def __init__(self):
        self.stt = SpeechToText()
        self.language_detector = LanguageDetector()
        self.nlp = NLPProcessor()
        self.entity_extractor = EntityExtractor()
        self.conversation = ConversationManager()
        self.tts = TextToSpeech()

    def process_text(
        self,
        text,
        language_code="en",
        language_confidence=1.0
    ):
        # 1. Detect language
        language_result = self.language_detector.detect(
            language_code,
            language_confidence
        )

        # 2. Process NLP
        nlp_result = self.nlp.process(text)

        # 3. Extract entities
        entity_result = self.entity_extractor.process(text)

        # 4. Combine extracted information
        extracted_data = {
            "name": entity_result["name"],
            "education": entity_result["education"],
            "skills": nlp_result["skills"],
            "experience": entity_result["experience"],
            "location": entity_result["location"],
            "intent": nlp_result["intent"],
            "job_domain": nlp_result["job_domain"],
            "job_preference": entity_result["job_preference"],
            "expected_salary": entity_result["expected_salary"],
            "language": language_result["language_code"]
        }

        # 5. Update beneficiary profile
        self.conversation.update_profile(extracted_data)

        # 6. Check profile completion
        profile_complete = self.conversation.is_profile_complete()

        # 7. Generate next question
        next_question = self.conversation.get_next_question(
            language_result["language_code"]
        )

        # 8. Generate TTS audio for next question
        tts_result = None

        if next_question:
            tts_result = self.tts.generate_audio(
                next_question,
                language_result["language_code"]
            )
            if tts_result["success"]:
                self.tts.play_audio(
                tts_result["audio_file"]
            )

        # 9. Return complete pipeline result
        return {
            "transcription": text,
            "language": language_result,
            "nlp": nlp_result,
            "entities": entity_result,
            "profile": self.conversation.get_profile(),
            "profile_complete": profile_complete,
            "next_question": next_question,
            "tts": tts_result
        }

    def process_audio(self, audio_file):
        # 1. Convert audio to text using Faster-Whisper
        stt_result = self.stt.transcribe(audio_file)

        # 2. Continue through the complete voice pipeline
        return self.process_text(
            text=stt_result["text"],
            language_code=stt_result["language"],
            language_confidence=stt_result["language_probability"]
        )


if __name__ == "__main__":

    pipeline = VoicePipeline()

    result = pipeline.process_audio("sample.m4a")

    print("\nTranscription:")
    print(result["transcription"])

    print("\nLanguage:")
    print(result["language"])

    print("\nNLP:")
    print(result["nlp"])

    print("\nEntities:")
    print(result["entities"])

    print("\nBeneficiary Profile:")
    print(result["profile"])

    print("\nProfile Complete:")
    print(result["profile_complete"])

    print("\nNext Question:")
    print(result["next_question"])

    print("\nTTS:")
    print(result["tts"])