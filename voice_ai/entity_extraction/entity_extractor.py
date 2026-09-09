import re


class EntityExtractor:

    def extract_experience(self, text):
        patterns = [
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:of)?\s*experience",
            r"experience\s*(?:of)?\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower())

            if match:
                return f"{match.group(1)} years"

        return None

    def extract_education(self, text):
        education_patterns = {
            "B.E": r"\bB\.?E\.?\b",
            "B.Tech": r"\bB\.?Tech\.?\b",
            "Bachelor": r"\bBachelor(?:'s)?\b",
            "M.E": r"\bM\.?E\.?\b",
            "M.Tech": r"\bM\.?Tech\.?\b",
            "Master": r"\bMaster(?:'s)?\b",
            "Diploma": r"\bDiploma\b",
            "ITI": r"\bITI\b",
            "12th": r"\b12th\b",
            "10th": r"\b10th\b"
        }

        detected = []

        for education, pattern in education_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(education)

        return detected

    def extract_location(self, text):
        location_patterns = [
            r"\bjobs?\s+in\s+([A-Z][a-zA-Z]+)",
            r"\bwork\s+in\s+([A-Z][a-zA-Z]+)",
            r"\blive\s+in\s+([A-Z][a-zA-Z]+)",
            r"\bbased\s+in\s+([A-Z][a-zA-Z]+)",
            r"\bfrom\s+([A-Z][a-zA-Z]+)"
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text)

            if match:
                return match.group(1)

        return None

    def extract_name(self, text):
        patterns = [
            r"\bmy name is ([A-Za-z]+(?:\s+[A-Za-z]+)*)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return match.group(1).strip()

        return None

    def extract_job_preference(self, text):
        preferences = {
            "remote": [
                "remote",
                "work from home",
                "wfh"
            ],
            "on_site": [
                "on site",
                "onsite",
                "office"
            ],
            "hybrid": [
                "hybrid"
            ]
        }

        text_lower = text.lower()

        for preference, keywords in preferences.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return preference

        return None

    def extract_salary(self, text):
        patterns = [
            r"(?:salary|pay|package)\s*(?:of|around|expected)?\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",
            r"(?:₹|rs\.?|inr)\s*([\d,]+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return match.group(1)

        return None

    def process(self, text):
        return {
            "name": self.extract_name(text),
            "experience": self.extract_experience(text),
            "education": self.extract_education(text),
            "location": self.extract_location(text),
            "job_preference": self.extract_job_preference(text),
            "expected_salary": self.extract_salary(text)
        }


if __name__ == "__main__":

    extractor = EntityExtractor()

    text = (
        "My name is Ravi Kumar. "
        "I have 2 years of experience in Python and Java. "
        "I completed my B.Tech. "
        "I am looking for software development jobs in Bangalore. "
        "I prefer hybrid work and expect a salary of 50000."
    )

    result = extractor.process(text)

    print("\n--- ANVESH AI Entity Extraction ---")
    print("Input:", text)
    print("Name:", result["name"])
    print("Experience:", result["experience"])
    print("Education:", result["education"])
    print("Location:", result["location"])
    print("Job Preference:", result["job_preference"])
    print("Expected Salary:", result["expected_salary"])