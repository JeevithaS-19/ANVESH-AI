import re


class EntityExtractor:

    # ============================================================
    # EDUCATION ALIASES
    # ============================================================

    EDUCATION_ALIASES = {
        "B.Tech": [
            "b.tech", "btech", "b tech", "bachelor of technology",
            "bachelor's of technology", "bachelors of technology",
        ],
        "B.E": [
            "b.e", "be", "b e", "bachelor of engineering",
            "bachelor's of engineering", "bachelors of engineering",
        ],
        "BCA": [
            "bca", "b c a", "bachelor of computer applications",
        ],
        "B.Sc": [
            "b.sc", "bsc", "b sc", "bachelor of science",
        ],
        "B.Com": [
            "b.com", "bcom", "b com", "bachelor of commerce",
        ],
        "BBA": [
            "bba", "b b a", "bachelor of business administration",
        ],
        "MBA": [
            "mba", "m b a", "master of business administration",
        ],
        "MCA": [
            "mca", "m c a", "master of computer applications",
        ],
        "M.Tech": [
            "m.tech", "mtech", "m tech", "master of technology",
        ],
        "M.E": [
            "m.e", "me", "m e", "master of engineering",
        ],
        "Diploma": [
            "diploma", "diploma course", "polytechnic",
        ],
        "12th": [
            "12th", "12 th", "twelfth", "higher secondary", "puc",
            "pre university", "pre-university",
        ],
        "10th": [
            "10th", "10 th", "tenth", "sslc",
        ],
        "MBBS": [
            "mbbs", "m b b s", "bachelor of medicine",
        ],
        "B.Ed": [
            "b.ed", "bed", "b ed", "bachelor of education",
        ],
    }

    # ============================================================
    # SKILL ALIASES
    # ============================================================

    SKILL_ALIASES = {
        "Python": ["python"],
        "Java": ["java"],
        "C": ["c"],
        "C++": ["c++", "cpp"],
        "C#": ["c#", "c sharp"],
        "JavaScript": ["javascript", "java script", "js"],
        "TypeScript": ["typescript", "type script", "ts"],
        "HTML": ["html", "hypertext markup language"],
        "CSS": ["css", "cascading style sheets"],
        "React": ["react", "react.js", "reactjs"],
        "Node.js": ["node.js", "nodejs", "node js"],
        "Express": ["express", "express.js", "expressjs"],
        "Django": ["django"],
        "Flask": ["flask"],
        "FastAPI": ["fastapi", "fast api"],
        "SQL": ["sql", "structured query language"],
        "MySQL": ["mysql", "my sql"],
        "PostgreSQL": ["postgresql", "postgres", "postgre sql"],
        "MongoDB": ["mongodb", "mongo db"],
        "Git": ["git"],
        "GitHub": ["github", "git hub"],
        "Docker": ["docker"],
        "Machine Learning": ["machine learning", "machine-learning", "ml"],
        "Artificial Intelligence": ["artificial intelligence", "artificial-intelligence", "ai"],
        "Natural Language Processing": ["natural language processing", "natural-language processing", "nlp"],
        "TensorFlow": ["tensorflow", "tensor flow"],
        "PyTorch": ["pytorch", "py torch"],
        "NumPy": ["numpy", "num py"],
        "Pandas": ["pandas"],
        "Matplotlib": ["matplotlib"],
        "OpenCV": ["opencv", "open cv"],
        "Communication": ["communication", "communication skills"],
        "Leadership": ["leadership", "leadership skills"],
        "Teamwork": ["teamwork", "team work"],
    }

    # ============================================================
    # LOCATION ALIASES
    # ============================================================

    LOCATION_ALIASES = {
        "Bangalore": ["bangalore", "bengaluru", "ಬೆಂಗಳೂರು", "ಬೆಂಗಳೂರು ನಗರ", "ಬೆಂಗಳೂರಿನಲ್ಲಿ"],
        "Mysore": ["mysore", "mysuru", "ಮೈಸೂರು", "ಮೈಸೂರಿನಲ್ಲಿ"],
        "Mangalore": ["mangalore", "mangaluru", "ಮಂಗಳೂರು", "ಮಂಗಳೂರಿನಲ್ಲಿ"],
        "Hubli": ["hubli", "hubballi", "ಹುಬ್ಬಳ್ಳಿ", "ಹುಬ್ಬಳ್ಳಿಯಲ್ಲಿ"],
        "Belgaum": ["belgaum", "belagavi", "ಬೆಳಗಾವಿ", "ಬೆಳಗಾವಿಯಲ್ಲಿ"],
        "Chennai": ["chennai", "madras", "ಚೆನ್ನೈ"],
        "Hyderabad": ["hyderabad", "ಹೈದರಾಬಾದ್"],
        "Mumbai": ["mumbai", "bombay", "ಮುಂಬೈ"],
        "Delhi": ["delhi", "new delhi", "ದೆಹಲಿ"],
        "Pune": ["pune", "ಪುಣೆ"],
        "Kolkata": ["kolkata", "calcutta", "ಕೊಲ್ಕತ್ತಾ"],
        "India": ["india", "ಭಾರತ", "भारत"],
    }

    # ============================================================
    # JOB PREFERENCES
    # ============================================================

    JOB_PREFERENCES = {
        "full-time": ["full time", "full-time", "fulltime"],
        "part-time": ["part time", "part-time", "parttime"],
        "remote": ["remote", "work from home", "wfh"],
        "hybrid": ["hybrid"],
        "internship": ["internship", "intern"],
    }

    def __init__(self):
        pass

    # ============================================================
    # SAFE ALIAS MATCHING
    # ============================================================

    def _contains_alias(self, text, alias):
        text_lower = text.lower()
        alias_lower = alias.lower()

        if any(ord(char) > 127 for char in alias_lower):
            return alias_lower in text_lower

        pattern = rf"(?:^|(?<=[^a-zA-Z0-9]))" + re.escape(alias_lower) + rf"(?:(?=[^a-zA-Z0-9])|$)"
        return re.search(pattern, text_lower) is not None

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

        # Numeric experience
        patterns = [
            r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
            r"(?:have|got|with)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            r"experience\s*(?:of|is|:)?\s*(\d+(?:\.\d+)?)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    val = float(match.group(1))
                    return int(val) if val.is_integer() else val
                except ValueError:
                    pass

        # Spoken numbers
        word_numbers = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        }

        for word, number in word_numbers.items():
            pattern = rf"\b{word}\s+(?:years?|yrs?)"
            if re.search(pattern, text_lower):
                return number

        # Fresher checks
        fresher_patterns = [
            "fresher", "fresh graduate", "no experience", "no work experience",
            "i have no experience", "i don't have experience", "i do not have experience",
            "ಅನುಭವ ಇಲ್ಲ", "ಅನುಭವವಿಲ್ಲ",
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

        return ", ".join(locations)

    # ============================================================
    # NAME
    # ============================================================

    def extract_name(self, text):
        text_original = text.strip()
        text_lower = text_original.lower()

        blocked_exact = {
            "i am a fresher", "i'm a fresher", "i am fresher", "i'm fresher",
            "i am a fresh graduate", "i'm a fresh graduate", "i have no experience",
        }

        if text_lower in blocked_exact:
            return None

        patterns = [
            r"\bmy name is\s+([A-Za-z][A-Za-z .'-]{1,50})",
            r"\bmy name's\s+([A-Za-z][A-Za-z .'-]{1,50})",
            r"\bname is\s+([A-Za-z][A-Za-z .'-]{1,50})",
            r"\bcall me\s+([A-Za-z][A-Za-z .'-]{1,50})",
        ]

        blocked_words = {
            "a", "an", "the", "fresher", "fresh", "graduate", "student", "looking",
            "for", "software", "developer", "development", "job", "work", "experience",
        }

        for pattern in patterns:
            match = re.search(pattern, text_original, flags=re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                name = re.split(r"\s+(?:and|but|from|in|with|for)\s+", name, flags=re.IGNORECASE)[0].strip()
                words = name.split()
                if words and not any(w.lower().strip(".,!?") in blocked_words for w in words):
                    return name

        match = re.match(r"^\s*i\s+am\s+([A-Za-z][A-Za-z .'-]{1,50})\s*$", text_original, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            words = candidate.split()
            if words and not any(w.lower().strip(".,!?") in blocked_words for w in words):
                return candidate

        return None

    # ============================================================
    # JOB PREFERENCE & SALARY
    # ============================================================

    def extract_job_preference(self, text):
        for preference, aliases in self.JOB_PREFERENCES.items():
            for alias in aliases:
                if self._contains_alias(text, alias):
                    return preference
        return None

    def extract_expected_salary(self, text):
        text_lower = text.lower()
        patterns = [
            r"(\d+(?:\.\d+)?)\s*(?:lpa|lakh|lakhs)",
            r"(\d+(?:\.\d+)?)\s*k\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = float(match.group(1))
                    if "lpa" in match.group(0) or "lakh" in match.group(0):
                        return value * 100000
                    if "k" in match.group(0):
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