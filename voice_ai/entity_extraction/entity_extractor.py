import re


class EntityExtractor:

    # ============================================================
    # EDUCATION
    # ============================================================

    EDUCATION_ALIASES = {

        "B.Tech": [
            "b.tech",
            "btech",
            "b tech",
            "bachelor of technology",
            "bachelor's of technology",
            "bachelors of technology",
            "be tech",
            "bee tech",
            "b tech degree",
            "b tick",
            "be tick",
            "b ticked",
            "be ticked",
            "b tek",
            "be tek",
        ],

        "B.E": [
            "b.e",
            "be",
            "b e",
            "bachelor of engineering",
            "bachelor's of engineering",
            "bachelors of engineering",
        ],

        "BCA": [
            "bca",
            "b c a",
            "bachelor of computer applications",
        ],

        "B.Sc": [
            "b.sc",
            "bsc",
            "b sc",
            "bachelor of science",
        ],

        "B.Com": [
            "b.com",
            "bcom",
            "b com",
            "bachelor of commerce",
        ],

        "BBA": [
            "bba",
            "b b a",
            "bachelor of business administration",
        ],

        "MBA": [
            "mba",
            "m b a",
            "master of business administration",
        ],

        "MCA": [
            "mca",
            "m c a",
            "master of computer applications",
        ],

        "M.Tech": [
            "m.tech",
            "mtech",
            "m tech",
            "master of technology",
        ],

        "M.E": [
            "m.e",
            "me",
            "m e",
            "master of engineering",
        ],

        "Diploma": [
            "diploma",
            "diploma course",
            "polytechnic",
        ],

        "12th": [
            "12th",
            "12 th",
            "twelfth",
            "higher secondary",
            "puc",
            "pre university",
            "pre-university",
        ],

        "10th": [
            "10th",
            "10 th",
            "tenth",
            "sslc",
        ],

        "MBBS": [
            "mbbs",
            "m b b s",
            "bachelor of medicine",
        ],

        "B.Ed": [
            "b.ed",
            "bed",
            "b ed",
            "bachelor of education",
        ],
    }

    # ============================================================
    # SKILLS
    # ============================================================

    SKILL_ALIASES = {

        # IT / Software
        "Python": ["python", "python3", "py", "paitan", "payton", "pythan", "py thon"],
        "Java": ["java", "core java", "j2ee", "jawa", "jaba", "jeeva"],
        "JavaScript": ["javascript", "java script", "js", "es6", "java scrip"],
        "HTML": ["html", "html5", "h t m l"],
        "CSS": ["css", "css3", "c s s"],
        "SQL": ["sql", "mysql", "structured query language", "s q l"],
        "Data Structures": [
            "data structures", "data structure", "dsa",
            "data structures and algorithms", "data structure algorithms"
        ],
        "REST APIs": [
            "rest apis", "rest api", "restful apis", "restful services",
            "api development", "api development skills"
        ],
        "Web Development": [
            "web development", "web dev", "web developer",
            "full stack development", "full stack", "web development skills"
        ],
        "Git/Version Control": [
            "git", "github", "git hub", "version control",
            "git version control", "git and github"
        ],
        "Cloud Basics": [
            "cloud basics", "cloud computing", "aws basics", "cloud", "aws"
        ],

        # Data / Analytics
        "Excel": ["excel", "ms excel", "microsoft excel", "spreadsheets", "spreadsheet"],
        "Data Analysis": ["data analysis", "data analytics", "analytics"],
        "Data Visualization": [
            "data visualization", "data visualisation", "dashboards",
            "power bi", "tableau"
        ],
        "Statistics": ["statistics", "statistical analysis", "statistical"],

        # Digital Marketing
        "Digital Marketing": ["digital marketing", "online marketing"],
        "SEO": ["seo", "search engine optimization", "search engine optimisation"],
        "Social Media Marketing": ["social media marketing", "smm", "social media"],
        "Content Writing": ["content writing", "copywriting", "content writer"],

        # Common / soft skills
        "Communication Skills": [
            "communication skills", "communication", "verbal communication",
            "soft skills", "good communication"
        ],

        # IT Support
        "Networking Basics": [
            "networking basics", "computer networking", "networking",
            "network basics"
        ],
        "Troubleshooting": [
            "troubleshooting", "technical troubleshooting", "technical support"
        ],
        "Customer Support": [
            "customer support", "customer service", "helpdesk", "help desk"
        ],

        # Design
        "UI/UX Design": [
            "ui ux design", "ui/ux design", "ui ux", "ui/ux",
            "user experience design", "product design", "user experience"
        ],
        "Graphic Design": ["graphic design", "visual design", "graphics"],

        # Retail
        "Retail Sales": [
            "retail sales", "sales associate skills", "sales associate",
            "retail"
        ],
        "Inventory Management": [
            "inventory management", "stock management", "inventory", "stock handling"
        ],
        "Cash Handling": ["cash handling", "billing", "cashier", "cash handling skills"],

        # Electrical
        "Electrical Wiring": [
            "electrical wiring", "wiring", "house wiring",
            "domestic wiring", "electric wiring"
        ],
        "Electrical Safety": [
            "electrical safety", "safety compliance", "electrical safe", "safety"
        ],
        "Basic Tool Handling": [
            "basic tool handling", "hand tools", "power tools",
            "tool handling", "tools"
        ],

        # Healthcare
        "Patient Care Basics": [
            "patient care basics", "patient care", "patient assistance",
            "bedside care"
        ],
        "First Aid": [
            "first aid", "basic life support", "bls", "first-aid"
        ],
    }

    # ============================================================
    # LOCATION
    # ============================================================

    LOCATION_ALIASES = {

        "Bangalore": [
            "bangalore",
            "bengaluru",
            "ಬೆಂಗಳೂರು",
            "ಬೆಂಗಳೂರು ನಗರ",
            "ಬೆಂಗಳೂರಿನಲ್ಲಿ",
            "ಬೆಂಗಳೂರಿನ",
            "ಬೆಂಗಳೂರಿಗೆ",
            "ಬೆಂಗಳೂರಿನಿಂದ",
        ],

        "Mysore": [
            "mysore",
            "mysuru",
            "ಮೈಸೂರು",
            "ಮೈಸೂರಿನಲ್ಲಿ",
            "ಮೈಸೂರಿನ",
        ],

        "Mangalore": [
            "mangalore",
            "mangaluru",
            "ಮಂಗಳೂರು",
            "ಮಂಗಳೂರಿನಲ್ಲಿ",
            "ಮಂಗಳೂರಿನ",
        ],

        "Hubli": [
            "hubli",
            "hubballi",
            "ಹುಬ್ಬಳ್ಳಿ",
            "ಹುಬ್ಬಳ್ಳಿಯಲ್ಲಿ",
        ],

        "Belgaum": [
            "belgaum",
            "belagavi",
            "ಬೆಳಗಾವಿ",
            "ಬೆಳಗಾವಿಯಲ್ಲಿ",
        ],

        "Chennai": [
            "chennai",
            "madras",
            "ಚೆನ್ನೈ",
        ],

        "Hyderabad": [
            "hyderabad",
            "ಹೈದರಾಬಾದ್",
        ],

        "Mumbai": [
            "mumbai",
            "bombay",
            "ಮುಂಬೈ",
        ],

        "Delhi": [
            "delhi",
            "new delhi",
            "ದೆಹಲಿ",
        ],

        "Pune": [
            "pune",
            "ಪುಣೆ",
        ],

        "Kolkata": [
            "kolkata",
            "calcutta",
            "ಕೊಲ್ಕತ್ತಾ",
        ],

        "India": [
            "india",
            "ಭಾರತ",
            "भारत",
        ],
    }

    # ============================================================
    # JOB PREFERENCES
    # ============================================================

    JOB_PREFERENCES = {

        "full-time": [
            "full time",
            "full-time",
            "fulltime",
        ],

        "part-time": [
            "part time",
            "part-time",
            "parttime",
        ],

        "remote": [
            "remote",
            "work from home",
            "wfh",
        ],

        "hybrid": [
            "hybrid",
        ],

        "internship": [
            "internship",
            "intern",
        ],
    }

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):
        pass

    # ============================================================
    # SAFE ALIAS MATCHING
    # ============================================================

    def _contains_alias(self, text, alias):

        text_lower = text.lower()
        alias_lower = alias.lower()

        # Unicode aliases
        if any(ord(char) > 127 for char in alias_lower):
            return alias_lower in text_lower

        pattern = (
            rf"(?<![a-zA-Z0-9])"
            rf"{re.escape(alias_lower)}"
            rf"(?![a-zA-Z0-9])"
        )

        return re.search(
            pattern,
            text_lower
        ) is not None

    # ============================================================
    # EDUCATION
    # ============================================================

    def extract_education(self, text):

        education = []

        for degree, aliases in self.EDUCATION_ALIASES.items():

            for alias in aliases:

                if self._contains_alias(text, alias):

                    if degree not in education:
                        education.append(degree)

                    break

        # Extra spoken-form fallbacks for Faster-Whisper output.
        if not education:
            value = re.sub(
                r"[^a-z]",
                "",
                text.lower()
            )

            if value in {
                "btech",
                "betech",
                "beetech",
                "btechdegree",
            }:
                education = ["B.Tech"]
            elif value in {
                "be",
                "bee",
            }:
                education = ["B.E"]
            elif value in {"bca", "beeay"}:
                education = ["BCA"]
            elif value in {"mca", "emseeay"}:
                education = ["MCA"]

        return education

    # ============================================================
    # SKILLS
    # ============================================================

    def extract_skills(self, text):

        skills = []

        for skill, aliases in self.SKILL_ALIASES.items():

            for alias in aliases:

                if self._contains_alias(text, alias):

                    if skill not in skills:
                        skills.append(skill)

                    break

        return skills

    # ============================================================
    # EXPERIENCE
    # ============================================================

    def extract_experience(self, text):

        text_lower = text.lower().strip()

        # --------------------------------------------------------
        # NUMERIC EXPERIENCE FIRST
        # --------------------------------------------------------
        # If the caller says something like:
        # "I have two years of experience"
        # "I am a fresher with two years of experience"
        # the explicit number is the useful value.
        patterns = [
            r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
            r"experience\s*(?:of|is|:)?\s*(\d+(?:\.\d+)?)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)

            if match:
                try:
                    value = float(match.group(1))

                    if value.is_integer():
                        return int(value)

                    return value

                except ValueError:
                    pass

        # --------------------------------------------------------
        # WORD-NUMBER EXPERIENCE
        # --------------------------------------------------------
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
        }

        for word, number in word_numbers.items():

            pattern = (
                rf"\b{word}\s+"
                rf"(?:years?|yrs?)"
            )

            if re.search(pattern, text_lower):
                return number

        # --------------------------------------------------------
        # FRESHER
        # --------------------------------------------------------
        fresher_patterns = [
            "fresher",
            "fresh graduate",
            "no experience",
            "no work experience",
            "i have no experience",
            "i don't have experience",
            "i do not have experience",
            "ಅನುಭವ ಇಲ್ಲ",
            "ಅನುಭವವಿಲ್ಲ",
        ]

        for pattern in fresher_patterns:
            if pattern in text_lower:
                return 0

        return None

    # ============================================================
    # LOCATION
    # ============================================================

    def extract_location(self, text):

        locations = []

        for location, aliases in self.LOCATION_ALIASES.items():

            for alias in aliases:

                if self._contains_alias(text, alias):
                    if location not in locations:
                        locations.append(location)
                    break

        if not locations:
            return None

        # Profile currently stores location as one field, so preserve
        # multiple requested cities in a readable string.
        return ", ".join(locations)

    # ============================================================
    # NAME
    # ============================================================

    def extract_name(self, text):

        text_original = text.strip()
        text_lower = text_original.lower()

        # Never treat these as names
        blocked_exact = {
            "i am a fresher",
            "i'm a fresher",
            "i am fresher",
            "i'm fresher",
            "i am a fresh graduate",
            "i'm a fresh graduate",
            "i have no experience",
            "i don't have experience",
            "i do not have experience",
        }

        if text_lower in blocked_exact:
            return None

        # --------------------------------------------------------
        # My name is Ravi
        # --------------------------------------------------------

        patterns = [
            r"\bmy name is\s+([A-Za-z][A-Za-z .'-]{1,50})",
            r"\bmy name's\s+([A-Za-z][A-Za-z .'-]{1,50})",
            r"\bname is\s+([A-Za-z][A-Za-z .'-]{1,50})",
            r"\bcall me\s+([A-Za-z][A-Za-z .'-]{1,50})",
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
            "software",
            "developer",
            "development",
            "job",
            "work",
            "experience",
            "engineer",
            "engineering",
        }

        for pattern in patterns:

            match = re.search(
                pattern,
                text_original,
                flags=re.IGNORECASE
            )

            if match:

                name = match.group(1).strip()

                name = re.split(
                    r"\s+(?:and|but|because|from|in|with|for)\s+",
                    name,
                    flags=re.IGNORECASE
                )[0].strip()

                words = name.split()

                if not words:
                    return None

                if any(
                    word.lower().strip(".,!?")
                    in blocked_words
                    for word in words
                ):
                    return None

                if all(
                    re.match(
                        r"^[A-Za-z][A-Za-z.'-]*$",
                        word
                    )
                    for word in words
                ):
                    return name

        # --------------------------------------------------------
        # I am Ravi
        # --------------------------------------------------------

        match = re.match(
            r"^\s*i\s+am\s+([A-Za-z][A-Za-z .'-]{1,50})\s*$",
            text_original,
            flags=re.IGNORECASE
        )

        if match:

            candidate = match.group(1).strip()
            candidate_lower = candidate.lower()

            if candidate_lower in {
                "a fresher",
                "fresher",
                "a fresh graduate",
                "fresh graduate",
                "a student",
                "student",
            }:
                return None

            words = candidate.split()

            if any(
                word.lower().strip(".,!?")
                in blocked_words
                for word in words
            ):
                return None

            if all(
                re.match(
                    r"^[A-Za-z][A-Za-z.'-]*$",
                    word
                )
                for word in words
            ):
                return candidate

        return None

    # ============================================================
    # JOB PREFERENCE
    # ============================================================

    def extract_job_preference(self, text):

        for preference, aliases in self.JOB_PREFERENCES.items():

            for alias in aliases:

                if self._contains_alias(text, alias):
                    return preference

        return None

    # ============================================================
    # EXPECTED SALARY
    # ============================================================

    def extract_expected_salary(self, text):

        text_lower = text.lower()

        patterns = [

            (
                r"(?:salary|pay|package|expecting|expected)"
                r".{0,30}?"
                r"(\d+(?:\.\d+)?)\s*"
                r"(?:lpa|lakh|lakhs)"
            ),

            (
                r"(\d+(?:\.\d+)?)\s*"
                r"(?:lpa|lakh|lakhs)"
            ),

            (
                r"(\d+(?:\.\d+)?)\s*k\b"
            ),
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text_lower
            )

            if match:

                try:

                    value = float(match.group(1))

                    if (
                        "lpa" in match.group(0)
                        or "lakh" in match.group(0)
                    ):
                        return value * 100000

                    if re.search(
                        r"\bk\b",
                        match.group(0)
                    ):
                        return value * 1000

                    return value

                except ValueError:
                    pass

        return None

    # ============================================================
    # MAIN PROCESS
    # ============================================================

    def process(self, text):

        if not text or not text.strip():

            return {
                "name": None,
                "education": [],
                "skills": [],
                "experience": None,
                "location": None,
                "job_preference": None,
                "expected_salary": None,
            }

        return {
            "name": self.extract_name(text),
            "education": self.extract_education(text),
            "skills": self.extract_skills(text),
            "experience": self.extract_experience(text),
            "location": self.extract_location(text),
            "job_preference": self.extract_job_preference(text),
            "expected_salary": self.extract_expected_salary(text),
        }


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":

    extractor = EntityExtractor()

    test_inputs = [
        "My name is Ravi",
        "I am Ravi Kumar",
        "I am a fresher",
        "I am fresher",
        "I have completed B.Tech",
        "I completed B.Tech and MBA",
        "I know Python and Java",
        "I know Python, Java, React and GitHub",
        "I have two years of experience",
        "I have 5 years of experience",
        "I am looking for opportunities in Bangalore",
        "ಬೆಂಗಳೂರು",
        "ನಾನು ಬೆಂಗಳೂರಿನಲ್ಲಿ ಕೆಲಸ ಹುಡುಕುತ್ತಿದ್ದೇನೆ",
        "ಬೆಂಗಳೂರಿನಲ್ಲಿ ಕೆಲಸ ಬೇಕು",
        "I want a remote job",
        "I am expecting 5 LPA",
        "I know AI, ML and NLP",
        "I know Git and GitHub",
        "I know JavaScript and TypeScript",
        "I know Python, Django, PostgreSQL and Docker",
    ]

    for text in test_inputs:

        result = extractor.process(text)

        print("\nINPUT:")
        print(text)

        print("\nEXTRACTED:")

        for key, value in result.items():
            print(f"{key}: {value}")

        print("-" * 60)