class ConversationManager:

    REQUIRED_FIELDS = [
        "name",
        "education",
        "skills",
        "experience",
        "location"
    ]

    QUESTIONS = {
        "en": {
            "name": "May I know your name?",
            "education": "What is your highest level of education?",
            "skills": "What skills do you have?",
            "experience": "How much work experience do you have?",
            "location": "Which location are you looking for opportunities in?"
        },

        "hi": {
            "name": "आपका नाम क्या है?",
            "education": "आपकी उच्चतम शैक्षणिक योग्यता क्या है?",
            "skills": "आपके पास कौन-कौन से कौशल हैं?",
            "experience": "आपके पास कितने वर्षों का कार्य अनुभव है?",
            "location": "आप किस स्थान पर अवसरों की तलाश कर रहे हैं?"
        },

        "kn": {
            "name": "ನಿಮ್ಮ ಹೆಸರು ಏನು?",
            "education": "ನಿಮ್ಮ ಅತ್ಯುನ್ನತ ಶೈಕ್ಷಣಿಕ ಅರ್ಹತೆ ಏನು?",
            "skills": "ನಿಮ್ಮ ಬಳಿ ಯಾವ ಕೌಶಲ್ಯಗಳಿವೆ?",
            "experience": "ನಿಮಗೆ ಎಷ್ಟು ವರ್ಷಗಳ ಕೆಲಸದ ಅನುಭವವಿದೆ?",
            "location": "ನೀವು ಯಾವ ಸ್ಥಳದಲ್ಲಿ ಉದ್ಯೋಗಾವಕಾಶಗಳನ್ನು ಹುಡುಕುತ್ತಿದ್ದೀರಿ?"
        }
    }

    def __init__(self):
        self.profile = {
            "name": None,
            "education": [],
            "skills": [],
            "experience": None,
            "location": None,
            "intent": None,
            "job_domain": None,
            "job_preference": None,
            "expected_salary": None,
            "language": "en"
        }

    def update_profile(self, extracted_data):
        for field, value in extracted_data.items():

            if value is None:
                continue

            if isinstance(value, list):

                if not value:
                    continue

                if isinstance(self.profile.get(field), list):

                    for item in value:
                        if item not in self.profile[field]:
                            self.profile[field].append(item)

                else:
                    self.profile[field] = value

            else:
                self.profile[field] = value

    def get_missing_field(self):
        for field in self.REQUIRED_FIELDS:

            value = self.profile.get(field)

            if value is None:
                return field

            if isinstance(value, list) and len(value) == 0:
                return field

        return None

    def get_next_question(self, language_code=None):

        missing_field = self.get_missing_field()

        if missing_field is None:
            return None

        language_code = language_code or self.profile.get("language", "en")

        # Fallback to English if the language is not supported
        if language_code not in self.QUESTIONS:
            language_code = "en"

        return self.QUESTIONS[language_code][missing_field]

    def is_profile_complete(self):
        return self.get_missing_field() is None

    def get_profile(self):
        return self.profile


if __name__ == "__main__":

    conversation = ConversationManager()

    print("\n--- ANVESH AI Conversation Flow Test ---")

    extracted_data = {
        "skills": ["Python", "Java"],
        "intent": "job_search",
        "job_domain": "Software Development",
        "language": "en"
    }

    conversation.update_profile(extracted_data)

    print("\nCollected Profile:")
    print(conversation.get_profile())

    print("\nIs Profile Complete?")
    print(conversation.is_profile_complete())

    print("\nNext Question:")
    print(conversation.get_next_question("en"))