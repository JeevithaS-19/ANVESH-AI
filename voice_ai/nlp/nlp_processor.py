import re


class NLPProcessor:

    INTENT_KEYWORDS = {
        "job_search": [
            "job",
            "jobs",
            "employment",
            "work",
            "vacancy",
            "career"
        ],
        "skill_development": [
            "learn",
            "learning",
            "course",
            "training",
            "skill",
            "skills",
            "upskill"
        ],
        "career_guidance": [
            "career",
            "career path",
            "career advice",
            "what should i become",
            "career guidance"
        ]
    }

    SKILLS = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "SQL",
        "MongoDB",
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "Web Development",
        "Cloud Computing",
        "Cybersecurity"
    ]

    JOB_DOMAINS = [
        "Software Development",
        "Web Development",
        "Data Science",
        "Machine Learning",
        "Artificial Intelligence",
        "Cybersecurity",
        "Cloud Computing"
    ]

    def detect_intent(self, text):
        text_lower = text.lower()

        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent

        return "general_query"

    def extract_skills(self, text):
        detected_skills = []

        for skill in self.SKILLS:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

            if re.search(pattern, text, re.IGNORECASE):
                detected_skills.append(skill)

        return detected_skills

    def extract_job_domain(self, text):
        text_lower = text.lower()

        for domain in self.JOB_DOMAINS:
            if domain.lower() in text_lower:
                return domain

        return None

    def process(self, text):
        return {
            "text": text,
            "intent": self.detect_intent(text),
            "skills": self.extract_skills(text),
            "job_domain": self.extract_job_domain(text)
        }


if __name__ == "__main__":

    processor = NLPProcessor()

    text = (
        "I'm looking for software development job. "
        "I have skills in Python Java and web development."
    )

    result = processor.process(text)

    print("Input:", result["text"])
    print("Intent:", result["intent"])
    print("Skills:", result["skills"])
    print("Job Domain:", result["job_domain"])