class ConversationManager:

    REQUIRED_FIELDS = [
        "name",
        "education",
        "skills",
        "experience",
        "location",
    ]

    QUESTIONS = {

        "en": {
            "name": "May I know your name?",
            "education": "What is your highest level of education?",
            "skills": "What skills do you have?",
            "experience": "How many years of experience do you have?",
            "location": "Which location are you looking for opportunities in?",
            "more_education": "Do you have any other educational qualifications?",
            "more_skills": "Do you have any other skills?",
        },

        "hi": {
            "name": "आपका नाम क्या है?",
            "education": "आपकी उच्चतम शैक्षणिक योग्यता क्या है?",
            "skills": "आपके पास कौन-कौन से कौशल हैं?",
            "experience": "आपके पास कितने वर्षों का अनुभव है?",
            "location": "आप किस स्थान पर अवसर ढूंढ रहे हैं?",
            "more_education": "क्या आपके पास कोई अन्य शैक्षणिक योग्यता है?",
            "more_skills": "क्या आपके पास कोई अन्य कौशल है?",
        },

        "kn": {
            "name": "ನಿಮ್ಮ ಹೆಸರನ್ನು ತಿಳಿಸಬಹುದೇ?",
            "education": "ನಿಮ್ಮ ಅತ್ಯುನ್ನತ ಶೈಕ್ಷಣಿಕ ಅರ್ಹತೆ ಏನು?",
            "skills": "ನಿಮ್ಮಲ್ಲಿರುವ ಕೌಶಲ್ಯಗಳು ಯಾವುವು?",
            "experience": "ನಿಮಗೆ ಎಷ್ಟು ವರ್ಷಗಳ ಅನುಭವವಿದೆ?",
            "location": "ನೀವು ಯಾವ ಸ್ಥಳದಲ್ಲಿ ಅವಕಾಶಗಳನ್ನು ಹುಡುಕುತ್ತಿದ್ದೀರಿ?",
            "more_education": "ನಿಮ್ಮಲ್ಲಿ ಬೇರೆ ಯಾವುದೇ ಶೈಕ್ಷಣಿಕ ಅರ್ಹತೆಗಳಿವೆಯೇ?",
            "more_skills": "ನಿಮ್ಮಲ್ಲಿ ಬೇರೆ ಯಾವುದೇ ಕೌಶಲ್ಯಗಳಿವೆಯೇ?",
        },
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
            "language": "en",
        }

        self.current_field = None

        self.education_collection_active = False
        self.education_confirmed = False

        self.skills_collection_active = False
        self.skills_confirmed = False

        self.language_locked = False

    # ============================================================
    # LANGUAGE
    # ============================================================

    def update_language(
        self,
        language_code,
        lock=False
    ):

        if language_code not in self.QUESTIONS:
            language_code = "en"

        self.profile["language"] = language_code

        if lock:
            self.language_locked = True

    # ============================================================
    # PROFILE UPDATE
    # ============================================================

    def update_profile(
        self,
        updates
    ):

        if not isinstance(updates, dict):
            return

        for field, value in updates.items():

            if field not in self.profile:
                continue

            if value is None:
                continue

            if field in ["education", "skills"]:

                if not isinstance(value, list):
                    value = [value]

                existing = self.profile[field]

                for item in value:

                    if (
                        item
                        and item not in existing
                    ):
                        existing.append(item)

            else:

                self.profile[field] = value

    # ============================================================
    # EDUCATION
    # ============================================================

    def ask_more_education(self):

        self.education_collection_active = True
        self.education_confirmed = False
        self.current_field = "more_education"

    def confirm_no_more_education(self):

        self.education_collection_active = False
        self.education_confirmed = True

        if self.profile["skills"]:
            if not self.skills_confirmed:
                self.current_field = "more_skills"
            else:
                self.current_field = None
        else:
            self.current_field = "skills"

    # ============================================================
    # SKILLS
    # ============================================================

    def ask_more_skills(self):

        self.skills_collection_active = True
        self.skills_confirmed = False
        self.current_field = "more_skills"

    def confirm_no_more_skills(self):

        self.skills_collection_active = False
        self.skills_confirmed = True

        if self.profile["experience"] is None:
            self.current_field = "experience"

        elif not self.profile["location"]:
            self.current_field = "location"

        else:
            self.current_field = None

    # ============================================================
    # MISSING FIELD
    # ============================================================

    def get_missing_field(self):

        profile = self.profile

        # --------------------------------------------------------
        # Name
        # --------------------------------------------------------

        if not profile["name"]:
            return "name"

        # --------------------------------------------------------
        # Education
        # --------------------------------------------------------

        if not profile["education"]:
            return "education"

        if (
            profile["education"]
            and not self.education_confirmed
        ):
            return "more_education"

        # --------------------------------------------------------
        # Skills
        # --------------------------------------------------------

        if not profile["skills"]:
            return "skills"

        if (
            profile["skills"]
            and not self.skills_confirmed
        ):
            return "more_skills"

        # --------------------------------------------------------
        # Experience
        # --------------------------------------------------------

        if profile["experience"] is None:
            return "experience"

        # --------------------------------------------------------
        # Location
        # --------------------------------------------------------

        if not profile["location"]:
            return "location"

        return None

    # ============================================================
    # NEXT QUESTION
    # ============================================================

    def get_next_question(self):

        missing = self.get_missing_field()

        self.current_field = missing

        if missing is None:
            return None

        language = self.profile.get(
            "language",
            "en"
        )

        questions = self.QUESTIONS.get(
            language,
            self.QUESTIONS["en"]
        )

        return questions.get(
            missing
        )

    # ============================================================
    # CURRENT FIELD
    # ============================================================

    def get_current_field(self):

        if self.current_field:
            return self.current_field

        return self.get_missing_field()

    # ============================================================
    # COMPLETE
    # ============================================================

    def is_profile_complete(self):

        profile = self.profile

        return bool(
            profile["name"]
            and profile["education"]
            and profile["skills"]
            and profile["experience"] is not None
            and profile["location"]
        )

    # ============================================================
    # GET PROFILE
    # ============================================================

    def get_profile(self):

        return {
            "name": self.profile["name"],
            "education": list(
                self.profile["education"]
            ),
            "skills": list(
                self.profile["skills"]
            ),
            "experience": self.profile["experience"],
            "location": self.profile["location"],
            "intent": self.profile["intent"],
            "job_domain": self.profile["job_domain"],
            "job_preference": self.profile["job_preference"],
            "expected_salary": self.profile["expected_salary"],
            "language": self.profile["language"],
        }

    # ============================================================
    # RESET
    # ============================================================

    def reset(self):

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
            "language": "en",
        }

        self.current_field = None

        self.education_collection_active = False
        self.education_confirmed = False

        self.skills_collection_active = False
        self.skills_confirmed = False

        self.language_locked = False