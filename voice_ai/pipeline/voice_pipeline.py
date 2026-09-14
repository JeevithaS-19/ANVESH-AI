import re

from voice_ai.speech_to_text.stt import SpeechToText
from voice_ai.language_detection.language_detector import LanguageDetector
from voice_ai.nlp.nlp_processor import NLPProcessor
from voice_ai.entity_extraction.entity_extractor import EntityExtractor
from voice_ai.conversation.conversation_manager import ConversationManager
from voice_ai.tts.text_to_speech import TextToSpeech


class VoicePipeline:

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        self.stt = SpeechToText()

        self.language_detector = (
            LanguageDetector()
        )

        self.nlp = NLPProcessor()

        self.entity_extractor = (
            EntityExtractor()
        )

        self.conversation = (
            ConversationManager()
        )

        self.tts = TextToSpeech()

        # ========================================================
        # NAME IS OPTIONAL FOR IVR DEMO
        # ========================================================
        #
        # We don't make name recognition block the IVR flow.
        # The caller can proceed directly to education.
        #

        # IVR DEMO: collect the caller's name instead of using a placeholder.
        # IVR DEMO: collect the caller name.
        self.conversation.profile["name"] = None

        self._skip_name = False

    # ============================================================
    # SCRIPT LANGUAGE DETECTION
    # ============================================================

    def detect_script_language(
        self,
        text
    ):

        if not text:
            return None

        # Kannada
        if any(
            "\u0C80" <= char <= "\u0CFF"
            for char in text
        ):
            return "kn"

        # Hindi / Devanagari
        if any(
            "\u0900" <= char <= "\u097F"
            for char in text
        ):
            return "hi"

        return None

    # ============================================================
    # EXPLICIT LANGUAGE COMMAND
    # ============================================================

    def detect_explicit_language(
        self,
        text
    ):

        text_lower = (
            text.lower()
            .strip()
        )

        kannada_commands = [
            "speak in kannada",
            "talk in kannada",
            "speak kannada",
            "talk kannada",
            "kannada",
            "ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಿ",
            "ಕನ್ನಡದಲ್ಲಿ",
            "ಕನ್ನಡ",
        ]

        for command in kannada_commands:

            if command in text_lower:
                return "kn"

        hindi_commands = [
            "speak in hindi",
            "talk in hindi",
            "speak hindi",
            "talk hindi",
            "hindi",
            "हिंदी में बोलो",
            "हिंदी में",
            "हिंदी",
        ]

        for command in hindi_commands:

            if command in text_lower:
                return "hi"

        english_commands = [
            "speak in english",
            "talk in english",
            "speak english",
            "talk english",
        ]

        for command in english_commands:

            if command in text_lower:
                return "en"

        return None

    # ============================================================
    # LANGUAGE DETECTION
    # ============================================================

    def detect_language(
        self,
        text
    ):

        explicit = (
            self.detect_explicit_language(
                text
            )
        )

        if explicit:
            return explicit

        script = (
            self.detect_script_language(
                text
            )
        )

        if script:
            return script

        try:

            result = (
                self.language_detector.detect(
                    text
                )
            )

            if isinstance(
                result,
                dict
            ):

                language = result.get(
                    "language_code"
                )

                if language in [
                    "en",
                    "hi",
                    "kn"
                ]:

                    return language

        except Exception:
            pass

        return (
            self.conversation
            .profile
            .get(
                "language",
                "en"
            )
        )

    # ============================================================
    # YES
    # ============================================================

    def is_yes(
        self,
        text
    ):

        text_lower = (
            text.lower()
            .strip()
        )

        return text_lower in {
            "yes",
            "yeah",
            "yep",
            "yup",
            "sure",
            "correct",
            "haan",
            "हाँ",
            "ಹೌದು",
        }

    # ============================================================
    # NO
    # ============================================================

    def is_no(self, text):

        if not text:
            return False

        text_lower = text.lower().strip()

        exact_no_words = {
            "no",
            "nope",
            "nah",
            "not",
            "none",
            "nothing",
            "haan nahi",
            "नहीं",
            "न",
            "ಇಲ್ಲ",
            "ಬೇಡ",
        }

        if text_lower in exact_no_words:
            return True

        # Handle natural spoken responses such as:
        # "No, I don't have any other qualification."
        # "No I don't."
        # "No, nothing else."
        if text_lower.startswith("no "):
            return True

        if text_lower.startswith("no,"):
            return True

        if text_lower.startswith("no."):
            return True

        return False

    # ============================================================
    # STRICT CONTEXTUAL NAME
    # ============================================================

    def extract_contextual_name(
        self,
        text
    ):

        if not text:
            return None

        text = text.strip()

        text_lower = (
            text.lower()
        )

        blocked_phrases = [
            "i am a fresher",
            "i'm a fresher",
            "i am fresher",
            "i'm fresher",
            "i am a fresh graduate",
            "i'm a fresh graduate",
            "i am looking",
            "i'm looking",
            "i want",
            "i need",
            "i have",
            "i know",
        ]

        if text_lower in blocked_phrases:
            return None

        patterns = [

            r"^\s*my\s+name\s+is\s+([A-Za-z][A-Za-z .'-]{0,40})\s*[.!?,]?\s*$",

            r"^\s*my\s+name's\s+([A-Za-z][A-Za-z .'-]{0,40})\s*[.!?,]?\s*$",

            r"^\s*call\s+me\s+([A-Za-z][A-Za-z .'-]{0,40})\s*[.!?,]?\s*$",

            r"^\s*i\s+am\s+([A-Za-z][A-Za-z .'-]{0,30})\s*[.!?,]?\s*$",

            r"^\s*i'm\s+([A-Za-z][A-Za-z .'-]{0,30})\s*[.!?,]?\s*$",
        ]

        blocked_words = {
            "a",
            "an",
            "the",
            "fresher",
            "fresh",
            "graduate",
            "student",
            "looking",
            "for",
            "job",
            "jobs",
            "work",
            "career",
            "opportunity",
            "opportunities",
            "software",
            "development",
            "developer",
            "experience",
            "years",
            "year",
            "skills",
            "skill",
            "education",
            "degree",
            "python",
            "java",
            "javascript",
            "react",
            "bangalore",
            "bengaluru",
        }

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if not match:
                continue

            candidate = (
                match.group(1)
                .strip()
            )

            words = candidate.split()

            if not words:
                continue

            if any(
                word.lower()
                .strip(".,!?")
                in blocked_words
                for word in words
            ):
                continue

            if len(words) > 4:
                continue

            return candidate

        return None

    # ============================================================
    # SAFE NLP
    # ============================================================

    def run_nlp(
        self,
        text
    ):

        try:

            result = (
                self.nlp.process(
                    text
                )
            )

            if isinstance(
                result,
                dict
            ):

                return result

        except Exception:
            pass

        return {}

    # ============================================================
    # SAFE ENTITY EXTRACTION
    # ============================================================

    def extract_entities(
        self,
        text
    ):

        try:

            result = (
                self.entity_extractor.process(
                    text
                )
            )

            if isinstance(
                result,
                dict
            ):

                return result

        except Exception:
            pass

        return {
            "name": None,
            "education": [],
            "skills": [],
            "experience": None,
            "location": None,
            "job_preference": None,
            "expected_salary": None,
        }

    # ============================================================
    # MERGE SKILLS
    # ============================================================

    def merge_skills(
        self,
        *skill_lists
    ):

        merged = []

        for skill_list in skill_lists:

            if not skill_list:
                continue

            if isinstance(
                skill_list,
                str
            ):

                skill_list = [
                    skill_list
                ]

            for skill in skill_list:

                if (
                    skill
                    and skill not in merged
                ):

                    merged.append(
                        skill
                    )

        return merged

    # ============================================================
    # PROCESS TEXT
    # ============================================================

    def process_text(
        self,
        text
    ):
        """
        State-driven IVR processing.

        The current conversation field is authoritative. This prevents:
        - greetings such as "Hello" becoming a caller name
        - education answers being interpreted as skills/name
        - noisy Whisper output from changing unrelated profile fields
        - the same question from being skipped accidentally
        """
        if not text or not text.strip():
            return self._build_response()

        text = text.strip()
        current_field = self.conversation.get_current_field()

        # ------------------------------------------------------------
        # LANGUAGE
        # ------------------------------------------------------------
        explicit_language = self.detect_explicit_language(text)

        if explicit_language:
            self.conversation.update_language(
                explicit_language,
                lock=True
            )
            return self._build_response()

        if self.conversation.language_locked:
            language = self.conversation.profile.get("language", "en")
        else:
            language = self.detect_language(text)

        if language not in {"en", "hi", "kn"}:
            language = "en"

        self.conversation.update_language(
            language,
            lock=False
        )

        # ------------------------------------------------------------
        # EMPTY / OBVIOUSLY NOISY SHORT TRANSCRIPT
        # ------------------------------------------------------------
        if self.is_noise_transcription(text, current_field):
            return self._build_response()

        # ------------------------------------------------------------
        # NAME
        # ------------------------------------------------------------
        if current_field == "name":
            name = self.extract_contextual_name(text)

            if name:
                self.conversation.update_profile({
                    "name": name
                })
                self.conversation.current_field = "job_domain"
                return self._build_response()

            # Plain spoken name: accept only plausible names.
            # Greetings / common filler / technical words are rejected.
            cleaned = re.sub(
                r"[^A-Za-z .'-]",
                "",
                text
            ).strip()

            normalized = re.sub(r"\s+", " ", cleaned).strip()
            normalized_lower = normalized.lower()

            blocked = {
                "hello", "hi", "hey", "hello thank you",
                "thank you", "thanks", "yes", "yeah", "okay",
                "ok", "done", "good morning", "good evening",
                "good afternoon", "good", "i don't know",
                "dont know", "i do not know", "no",
                "b tech", "btech", "be", "b e", "b.e",
                "python", "java", "javascript", "react",
                "software", "developer", "development",
                "job", "jobs", "work", "fresher", "student"
            }

            words = normalized.split()

            if (
                1 <= len(words) <= 3
                and normalized_lower not in blocked
                and all(
                    re.fullmatch(
                        r"[A-Za-z][A-Za-z.'-]*",
                        word
                    )
                    for word in words
                )
                and any(char.isalpha() for char in normalized)
            ):
                self.conversation.update_profile({
                    "name": normalized
                })
                self.conversation.current_field = "job_domain"
                return self._build_response()

            # Do not store invalid speech as a name.
            return self._build_response()

        # ------------------------------------------------------------
        # JOB DOMAIN
        # ------------------------------------------------------------
        if current_field == "job_domain":
            job_text = text.lower()

            domain = None

            domain_patterns = [
                (
                    "Software Development",
                    [
                        "software development",
                        "software developer",
                        "software engineering",
                        "software engineer",
                        "developer",
                        "programmer",
                        "coding",
                        "software"
                    ]
                ),
                (
                    "Web Development",
                    [
                        "web development",
                        "web developer",
                        "website development",
                        "frontend",
                        "front end",
                        "backend",
                        "back end",
                        "full stack",
                        "fullstack"
                    ]
                ),
                (
                    "Data Science",
                    [
                        "data science",
                        "data scientist"
                    ]
                ),
                (
                    "Data",
                    [
                        "data analyst",
                        "data analysis",
                        "data"
                    ]
                ),
                (
                    "Cybersecurity",
                    [
                        "cybersecurity",
                        "cyber security",
                        "security",
                        "ethical hacking"
                    ]
                ),
                (
                    "Artificial Intelligence",
                    [
                        "artificial intelligence",
                        "artificial intelligence job",
                        "ai job",
                        "ai"
                    ]
                ),
                (
                    "Machine Learning",
                    [
                        "machine learning",
                        "machine learning job",
                        "ml"
                    ]
                ),
                (
                    "Software Testing",
                    [
                        "software testing",
                        "software tester",
                        "tester",
                        "testing"
                    ]
                ),
                (
                    "Python Development",
                    [
                        "python development",
                        "python developer",
                        "python"
                    ]
                )
            ]

            for canonical, aliases in domain_patterns:
                if any(alias in job_text for alias in aliases):
                    domain = canonical
                    break

            if domain is None:
                quick_entities = self.extract_entities(text)
                extracted_domain = quick_entities.get("job_domain")

                if extracted_domain:
                    invalid = {
                        "general", "jobs", "job", "work",
                        "opportunities", "general jobs"
                    }
                    if str(extracted_domain).strip().lower() not in invalid:
                        domain = extracted_domain

            # Never save arbitrary Whisper garbage as a job domain.
            if domain:
                self.conversation.profile["job_domain"] = domain
                self.conversation.current_field = "education"

            return self._build_response()

        # ------------------------------------------------------------
        # EDUCATION
        # ------------------------------------------------------------
        if current_field == "education":
            entities = self.extract_entities(text)
            education = entities.get("education", [])

            # Robust IVR aliases. Whisper commonly produces variants such
            # as "be ticked" for "B.Tech".
            education_text = text.lower().strip()
            normalized_education = re.sub(
                r"[^a-z0-9+#.\s-]",
                " ",
                education_text
            )
            normalized_education = re.sub(
                r"\s+",
                " ",
                normalized_education
            ).strip()

            fuzzy_education = [
                (
                    "B.Tech",
                    [
                        "b.tech", "btech", "b tech",
                        "bachelor of technology",
                        "be tech", "bee tech", "b tech degree",
                        "b tick", "be tick", "b ticked", "be ticked",
                        "b take", "be take", "b tek", "be tek",
                        "b tech degree"
                    ]
                ),
                (
                    "B.E",
                    [
                        "b.e", "b e", "be",
                        "bachelor of engineering",
                        "bee", "b eng", "be engineering"
                    ]
                ),
                (
                    "M.Tech",
                    [
                        "m.tech", "mtech", "m tech",
                        "master of technology",
                        "em tech", "em tech"
                    ]
                ),
                (
                    "M.E",
                    [
                        "m.e", "m e",
                        "master of engineering"
                    ]
                ),
                (
                    "BCA",
                    [
                        "bca", "b c a",
                        "bachelor of computer applications"
                    ]
                ),
                (
                    "MCA",
                    [
                        "mca", "m c a",
                        "master of computer applications"
                    ]
                ),
                (
                    "B.Sc",
                    [
                        "b.sc", "bsc", "b sc",
                        "bachelor of science"
                    ]
                ),
                (
                    "M.Sc",
                    [
                        "m.sc", "msc", "m sc",
                        "master of science"
                    ]
                ),
                (
                    "B.Com",
                    [
                        "b.com", "bcom", "b com",
                        "bachelor of commerce"
                    ]
                ),
                (
                    "BBA",
                    [
                        "bba", "b b a",
                        "bachelor of business administration"
                    ]
                ),
                (
                    "MBA",
                    [
                        "mba", "m b a",
                        "master of business administration"
                    ]
                ),
                (
                    "Diploma",
                    [
                        "diploma", "polytechnic"
                    ]
                ),
                (
                    "12th",
                    [
                        "12th", "12 th", "twelfth",
                        "plus two", "higher secondary", "puc",
                        "pre university", "pre-university"
                    ]
                ),
                (
                    "10th",
                    [
                        "10th", "10 th", "tenth", "sslc"
                    ]
                )
            ]

            if not education:
                for canonical, aliases in fuzzy_education:
                    if any(
                        alias in normalized_education
                        for alias in aliases
                    ):
                        education = [canonical]
                        break

            # Special compact Whisper fallbacks.
            compact = re.sub(
                r"[^a-z]",
                "",
                education_text
            )

            if not education:
                if compact in {
                    "btech", "betech", "beetech",
                    "btechdegree", "btechengineering"
                }:
                    education = ["B.Tech"]
                elif compact in {
                    "be", "bee", "beengineering"
                }:
                    education = ["B.E"]
                elif compact in {"bca", "beeay"}:
                    education = ["BCA"]
                elif compact in {"mca", "emseeay"}:
                    education = ["MCA"]

            if education:
                self.conversation.update_profile({
                    "education": education
                })
                self.conversation.education_collection_active = False
                self.conversation.education_confirmed = True
                self.conversation.current_field = "skills"

            return self._build_response()

        # ------------------------------------------------------------
        # SKILLS
        # ------------------------------------------------------------
        if current_field == "skills":
            entities = self.extract_entities(text)
            skills = self.merge_skills(
                entities.get("skills", [])
            )

            # Common spoken technical skills that may be missed by NLP.
            skill_aliases = {
                "Python": ["python"],
                "Java": ["java"],
                "C": [" c ", "c programming", "c language"],
                "C++": ["c++", "cpp"],
                "JavaScript": ["javascript", "java script"],
                "TypeScript": ["typescript", "type script"],
                "HTML": ["html"],
                "CSS": ["css"],
                "React": ["react", "reactjs", "react js"],
                "Node.js": ["node.js", "nodejs", "node js"],
                "SQL": ["sql"],
                "MongoDB": ["mongodb", "mongo db"],
                "Git": ["git"],
                "GitHub": ["github", "git hub"],
                "Docker": ["docker"],
                "Machine Learning": [
                    "machine learning", "machine-learning"
                ],
                "Artificial Intelligence": [
                    "artificial intelligence"
                ],
                "Communication": [
                    "communication", "communication skills"
                ],
                "Leadership": ["leadership"],
                "Teamwork": ["teamwork", "team work"]
            }

            padded = f" {text.lower()} "

            for skill, aliases in skill_aliases.items():
                if any(alias in padded for alias in aliases):
                    if skill not in skills:
                        skills.append(skill)

            if skills:
                self.conversation.update_profile({
                    "skills": skills
                })
                self.conversation.skills_collection_active = False
                self.conversation.skills_confirmed = True
                self.conversation.current_field = "experience"

            return self._build_response()

        # ------------------------------------------------------------
        # EXPERIENCE
        # ------------------------------------------------------------
        if current_field == "experience":
            entities = self.extract_entities(text)
            experience = entities.get("experience")

            if experience is None:
                experience = self.extract_experience_fallback(text)

            if experience is not None:
                self.conversation.update_profile({
                    "experience": f"{experience} years"
                })
                self.conversation.current_field = "location"

            return self._build_response()

        # ------------------------------------------------------------
        # LOCATION
        # ------------------------------------------------------------
        if current_field == "location":
            entities = self.extract_entities(text)
            location = entities.get("location")

            if location is None:
                location = self.extract_location_fallback(text)

            if location:
                self.conversation.update_profile({
                    "location": location
                })
                self.conversation.current_field = None

            return self._build_response()

        # ------------------------------------------------------------
        # OPTIONAL / UNKNOWN STATE
        # ------------------------------------------------------------
        self._advance_state()
        return self._build_response()

    # ============================================================
    # IVR SAFETY HELPERS
    # ============================================================

    def is_noise_transcription(
        self,
        text,
        current_field=None
    ):
        """Reject common Whisper filler/noise without changing profile."""
        if not text:
            return True

        value = re.sub(
            r"\s+",
            " ",
            text.lower().strip()
        )

        noise = {
            "",
            "done",
            "done!",
            "okay",
            "ok",
            "thanks",
            "thank you",
            "thank you.",
            "hello",
            "hi",
            "hey",
            "hmm",
            "um",
            "uh",
            "yeah",
            "yes"
        }

        if value in noise:
            # "yes" is meaningful only for an explicit confirmation
            # state, which this simplified IVR does not require.
            return True

        # Very short punctuation-only / symbol-heavy results.
        letters = sum(char.isalpha() for char in value)
        if letters == 0:
            return True

        # Obvious non-supported scripts from Whisper should not be
        # interpreted as English names, skills, or locations.
        if current_field == "name":
            if any(
                ord(char) > 127
                for char in value
            ):
                return True

        return False

    def extract_experience_fallback(self, text):
        """Extra IVR-friendly experience parsing."""
        value = text.lower().strip()

        word_numbers = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "no": 0
        }

        # Numeric values first.
        match = re.search(
            r"\b(\d+(?:\.\d+)?)\s*(?:\+?\s*)"
            r"(?:years?|yrs?)\b",
            value
        )
        if match:
            number = float(match.group(1))
            return int(number) if number.is_integer() else number

        # Spoken numbers.
        for word, number in word_numbers.items():
            if re.search(
                rf"\b{word}\s+(?:years?|yrs?)\b",
                value
            ):
                return number

        if any(
            phrase in value
            for phrase in {
                "no experience",
                "no work experience",
                "fresher",
                "fresh graduate",
                "zero experience"
            }
        ):
            return 0

        return None

    def extract_location_fallback(self, text):
        """Recognize common Indian opportunity locations."""
        value = text.lower()

        aliases = {
            "Bangalore": [
                "bangalore",
                "bengaluru",
                "bengalooru"
            ],
            "Mysore": [
                "mysore",
                "mysuru"
            ],
            "Mangalore": [
                "mangalore",
                "mangaluru"
            ],
            "Hubli": [
                "hubli",
                "hubballi"
            ],
            "Belgaum": [
                "belgaum",
                "belagavi"
            ],
            "Chennai": [
                "chennai",
                "madras"
            ],
            "Hyderabad": [
                "hyderabad"
            ],
            "Mumbai": [
                "mumbai",
                "bombay"
            ],
            "Delhi": [
                "delhi",
                "new delhi"
            ],
            "Pune": [
                "pune"
            ],
            "Kolkata": [
                "kolkata",
                "calcutta"
            ],
            "India": [
                "india"
            ]
        }

        found = []

        for city, city_aliases in aliases.items():
            if any(
                alias in value
                for alias in city_aliases
            ):
                if city not in found:
                    found.append(city)

        return ", ".join(found) if found else None

    # ============================================================
    # ADVANCE STATE
    # ============================================================

    def _advance_state(self):

        profile = self.conversation.profile

        # 1. NAME
        if not profile.get("name"):
            self.conversation.current_field = "name"
            return

        # 2. JOB TYPE / DOMAIN
        if not profile.get("job_domain"):
            self.conversation.current_field = "job_domain"
            return

        # 3. EDUCATION
        if not profile["education"]:
            self.conversation.current_field = "education"
            return

        self.conversation.education_confirmed = True
        self.conversation.education_collection_active = False

        # 4. SKILLS
        if not profile["skills"]:
            self.conversation.current_field = "skills"
            return

        self.conversation.skills_confirmed = True
        self.conversation.skills_collection_active = False

        # 5. EXPERIENCE
        if profile["experience"] is None:
            self.conversation.current_field = "experience"
            return

        # 6. LOCATION
        if not profile["location"]:
            self.conversation.current_field = "location"
            return

        # 7. COMPLETE
        self.conversation.current_field = None

    # ============================================================
    # PROCESS AUDIO
    # ============================================================

    def process_audio(
        self,
        audio_file
    ):

        stt_result = (
            self.stt.transcribe(
                audio_file
            )
        )

        text = stt_result.get(
            "text",
            ""
        )

        result = self.process_text(
            text
        )

        stt_language = (
            stt_result.get(
                "language"
            )
        )

        stt_probability = (
            stt_result.get(
                "language_probability"
            )
        )

        result["transcription"] = text

        result["stt_language"] = (
            stt_language
        )

        result[
            "stt_language_probability"
        ] = stt_probability

        return result

    # ============================================================
    # BUILD RESPONSE
    # ============================================================

    def _build_response(self):
        profile = self.conversation.get_profile()
        complete = self.conversation.is_profile_complete()

        next_question = None

        if not complete:
            field = self.conversation.get_current_field()

            # Keep the state deterministic.
            if not profile.get("name"):
                field = "name"
                self.conversation.current_field = "name"
            elif not profile.get("job_domain"):
                field = "job_domain"
                self.conversation.current_field = "job_domain"
            elif not profile.get("education"):
                field = "education"
                self.conversation.current_field = "education"
            elif not profile.get("skills"):
                field = "skills"
                self.conversation.current_field = "skills"
            elif profile.get("experience") is None:
                field = "experience"
                self.conversation.current_field = "experience"
            elif not profile.get("location"):
                field = "location"
                self.conversation.current_field = "location"

            questions = {
                "en": {
                    "name": "May I know your name?",
                    "job_domain": "What kind of job are you looking for?",
                    "education": "What is your highest level of education?",
                    "skills": "What skills do you have?",
                    "experience": "How many years of experience do you have?",
                    "location": "Which location are you looking for opportunities in?"
                },
                "hi": {
                    "name": "आपका नाम क्या है?",
                    "job_domain": "आप किस प्रकार की नौकरी की तलाश कर रहे हैं?",
                    "education": "आपकी उच्चतम शैक्षणिक योग्यता क्या है?",
                    "skills": "आपके पास कौन से कौशल हैं?",
                    "experience": "आपके पास कितने वर्षों का अनुभव है?",
                    "location": "आप किस स्थान पर अवसर चाहते हैं?"
                },
                "kn": {
                    "name": "ನಿಮ್ಮ ಹೆಸರು ಏನು?",
                    "job_domain": "ನೀವು ಯಾವ ರೀತಿಯ ಉದ್ಯೋಗವನ್ನು ಹುಡುಕುತ್ತಿದ್ದೀರಿ?",
                    "education": "ನಿಮ್ಮ ಅತ್ಯುನ್ನತ ಶೈಕ್ಷಣಿಕ ಅರ್ಹತೆ ಏನು?",
                    "skills": "ನಿಮ್ಮಲ್ಲಿರುವ ಕೌಶಲ್ಯಗಳು ಯಾವುವು?",
                    "experience": "ನಿಮಗೆ ಎಷ್ಟು ವರ್ಷಗಳ ಅನುಭವವಿದೆ?",
                    "location": "ನೀವು ಯಾವ ಸ್ಥಳದಲ್ಲಿ ಅವಕಾಶಗಳನ್ನು ಹುಡುಕುತ್ತಿದ್ದೀರಿ?"
                }
            }

            language_code = profile.get("language", "en")
            if language_code not in questions:
                language_code = "en"

            next_question = questions[language_code].get(field)

        tts_result = None

        if next_question:
            try:
                tts_result = self.tts.generate_audio(
                    next_question,
                    profile.get("language", "en")
                )
            except Exception as error:
                tts_result = {
                    "success": False,
                    "error": str(error)
                }

        language_code = profile.get("language", "en")

        language_names = {
            "en": "English",
            "hi": "Hindi",
            "kn": "Kannada"
        }

        return {
            "profile": profile,
            "language": {
                "language_code": language_code,
                "language": language_names.get(
                    language_code,
                    "English"
                )
            },
            "next_question": next_question,
            "profile_complete": complete,
            "tts": tts_result
        }

    # ============================================================
    # RESET
    # ============================================================

    def reset(self):

        self.conversation.reset()

        # Start every new IVR call from the beginning.
        self.conversation.profile["name"] = None
        self._skip_name = False
        self.conversation.current_field = "name"