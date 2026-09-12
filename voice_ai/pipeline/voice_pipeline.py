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

    def process_text(self, text, language_code="en", language_confidence=1.0):

        language_result = self.language_detector.detect(
            language_code,
            language_confidence
        )

        nlp_result = self.nlp.process(text)

        entity_result = self.entity_extractor.process(text)

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

        self.conversation.update_profile(extracted_data)

        profile_complete = self.conversation.is_profile_complete()
        next_question = self.conversation.get_next_question()
        if next_question:
            self.tts.speak(next_question)

        return {
            "transcription": text,
            "language": language_result,
            "nlp": nlp_result,
            "entities": entity_result,
            "profile": self.conversation.get_profile(),
            "profile_complete": profile_complete,
            "next_question": next_question
        }

    def process_audio(self, audio_file):

        stt_result = self.stt.transcribe(audio_file)

        return self.process_text(
            stt_result["text"],
            stt_result["language"],
            stt_result["language_probability"]
        )


if __name__ == "__main__":

    pipeline = VoicePipeline()

    result = pipeline.process_audio("sample.m4a")

    print("\n--- ANVESH AI VOICE PIPELINE ---")

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