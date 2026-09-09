class ConversationManager:

    REQUIRED_FIELDS = [
        "name",
        "education",
        "skills",
        "experience",
        "location"
    ]

    QUESTIONS = {
        "name": "May I know your name?",
        "education": "What is your highest level of education?",
        "skills": "What skills do you have?",
        "experience": "How much work experience do you have?",
        "location": "Which location are you looking for opportunities in?"
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
            "language": None
        }

    def update_profile(self, extracted_data):
        for field, value in extracted_data.items():

            if value is None:
                continue

            if isinstance(value, list):
                if value:
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

    def get_next_question(self):
        missing_field = self.get_missing_field()

        if missing_field is None:
            return None

        return self.QUESTIONS[missing_field]

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
        "job_domain": "Software Development"
    }

    conversation.update_profile(extracted_data)

    print("\nCollected Profile:")
    print(conversation.get_profile())

    print("\nIs Profile Complete?")
    print(conversation.is_profile_complete())

    print("\nNext Question:")
    print(conversation.get_next_question())