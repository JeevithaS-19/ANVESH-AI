import re

from recommendation_engine.skill_gap import calculate_skill_gap
from recommendation_engine.compatibility_score import calculate_compatibility_score


def calculate_education_match(user_education, required_education):
    """
    Compare beneficiary education with the occupation's
    education requirement.
    """

    if not user_education or not required_education:
        return 0

    user = user_education.lower().strip()
    required = " ".join(required_education).lower()

    # Direct match
    if user in required:
        return 100

    undergraduate_terms = [
        "b.tech",
        "btech",
        "b.e",
        "be ",
        "bca",
        "b.sc",
        "bsc",
        "b.com",
        "bcom",
        "graduate",
        "graduation"
    ]

    postgraduate_terms = [
        "m.tech",
        "mtech",
        "m.e",
        "me ",
        "mca",
        "m.sc",
        "msc",
        "m.com",
        "mcom",
        "postgraduate",
        "post graduation"
    ]

    diploma_terms = [
        "diploma",
        "polytechnic"
    ]

    iti_terms = [
        "iti",
        "industrial training institute"
    ]

    school_10_terms = [
        "10th",
        "10th pass",
        "sslc",
        "matriculation"
    ]

    school_12_terms = [
        "12th",
        "12th pass",
        "puc",
        "higher secondary"
    ]

    if any(term in user for term in postgraduate_terms):
        user_category = "postgraduate"

    elif any(term in user for term in undergraduate_terms):
        user_category = "graduate"

    elif any(term in user for term in diploma_terms):
        user_category = "diploma"

    elif any(term in user for term in iti_terms):
        user_category = "iti"

    elif any(term in user for term in school_12_terms):
        user_category = "12th"

    elif any(term in user for term in school_10_terms):
        user_category = "10th"

    else:
        user_category = "other"

    if user_category == "postgraduate":

        if (
            "postgraduate" in required
            or "post graduation" in required
            or "graduate" in required
        ):
            return 100

    if user_category == "graduate":

        if (
            "graduate" in required
            or "graduation" in required
            or "b.tech" in required
            or "btech" in required
            or "b.e" in required
            or "bca" in required
            or "b.sc" in required
            or "b.com" in required
        ):
            return 100

    if user_category == "diploma":

        if "diploma" in required or "certificate" in required:
            return 100

    if user_category == "iti":

        if "iti" in required or "vocational" in required:
            return 100

    if user_category == "12th":

        if (
            "12th" in required
            or "higher secondary" in required
            or "12th pass" in required
        ):
            return 100

    if user_category == "10th":

        if "10th" in required or "10th pass" in required:
            return 100

    if user_category in ["graduate", "postgraduate"]:

        if "any discipline" in required:
            return 100

    return 0


def calculate_interest_match(user_interests, occupation_name):
    """
    Match beneficiary interests with occupation-related keywords.

    This works without requiring an interests column
    in the SQLite database.
    """

    if not user_interests:
        return 0

    occupation_interests = {
        "data analyst": [
            "data",
            "data analysis",
            "analytics",
            "statistics",
            "numbers",
            "technology",
            "research",
            "excel",
            "sql"
        ],

        "software developer": [
            "software",
            "programming",
            "coding",
            "technology",
            "development",
            "computer",
            "applications"
        ],

        "digital marketing executive": [
            "marketing",
            "digital marketing",
            "social media",
            "content",
            "advertising",
            "communication"
        ],

        "web designer": [
            "web design",
            "web designer",
            "design",
            "ui",
            "ux",
            "graphics",
            "creative",
            "web development"
        ],

        "it support technician": [
            "technology",
            "computers",
            "technical support",
            "networking",
            "troubleshooting"
        ],

        "retail sales associate": [
            "sales",
            "retail",
            "business",
            "customers",
            "communication",
            "shopping"
        ],

        "domestic electrician": [
            "electrical",
            "electronics",
            "wiring",
            "repair",
            "tools",
            "technical work"
        ],

        "healthcare support worker": [
            "healthcare",
            "health care",
            "hospital",
            "patients",
            "medical",
            "helping people",
            "care"
        ]
    }

    occupation = occupation_name.lower().strip()

    required_interests = occupation_interests.get(
        occupation,
        []
    )

    if not required_interests:
        return 0

    matched = 0

    for user_interest in user_interests:

        interest = user_interest.lower().strip()

        for keyword in required_interests:

            if interest in keyword or keyword in interest:
                matched += 1
                break

    if matched == 0:
        return 0

    return min(
        100,
        round(
            (matched / len(user_interests)) * 100,
            2
        )
    )


def calculate_career_goal_match(career_goal, occupation):
    """
    Match the beneficiary's career goal with an occupation
    using occupation names and related career terms.
    """

    if not career_goal:
        return 0

    goal = career_goal.lower().strip()
    occupation_name = occupation.lower().strip()

    # Exact occupation match
    if occupation_name in goal:
        return 100

    career_keywords = {
        "data analyst": [
            "data",
            "analytics",
            "analyst",
            "data analysis",
            "business intelligence",
            "reporting"
        ],

        "software developer": [
            "software",
            "developer",
            "development",
            "programming",
            "software engineer",
            "application developer",
            "coding"
        ],

        "digital marketing executive": [
            "digital marketing",
            "marketing",
            "seo",
            "social media",
            "online marketing",
            "content marketing"
        ],

        "web designer": [
            "web design",
            "web designer",
            "website design",
            "ui design",
            "ux design",
            "ui/ux"
        ],

        "it support technician": [
            "it support",
            "technical support",
            "help desk",
            "helpdesk",
            "computer support",
            "it technician",
            "troubleshooting"
        ],

        "retail sales associate": [
            "retail",
            "sales",
            "retail sales",
            "store sales",
            "shop sales"
        ],

        "domestic electrician": [
            "electrician",
            "electrical",
            "electrical work",
            "wiring",
            "electric work"
        ],

        "healthcare support worker": [
            "healthcare",
            "health care",
            "hospital",
            "patient care",
            "medical support",
            "health worker"
        ]
    }

    keywords = career_keywords.get(
        occupation_name,
        []
    )

    matched_keywords = 0

    for keyword in keywords:

        if keyword in goal:
            matched_keywords += 1

    if matched_keywords >= 2:
        return 100

    if matched_keywords == 1:
        return 75

    return 0


def extract_years(text):
    """
    Extract numeric years from experience text.

    Examples:
    '1 year' -> 1
    '2 years' -> 2
    '3 yrs' -> 3
    """

    if not text:
        return None

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        text.lower()
    )

    if match:
        return float(match.group(1))

    return None


def calculate_experience_match(
    user_experience,
    required_experience
):
    """
    Compare beneficiary experience with
    the occupation's required experience range.
    """

    user_years = extract_years(user_experience)

    if user_years is None:
        return 0

    if not required_experience:
        return 0

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        required_experience
    )

    if not numbers:
        return 0

    if len(numbers) >= 2:

        minimum = float(numbers[0])
        maximum = float(numbers[1])

        if minimum <= user_years <= maximum:
            return 100

        if user_years < minimum:
            difference = minimum - user_years
        else:
            difference = user_years - maximum

        if difference <= 1:
            return 75

        if difference <= 2:
            return 50

        return 25

    required_years = float(numbers[0])

    if user_years >= required_years:
        return 100

    difference = required_years - user_years

    if difference <= 1:
        return 75

    if difference <= 2:
        return 50

    return 25


def match_occupation(
    user_skills,
    occupation,
    required_skills,
    education_match,
    experience_match,
    interest_match,
    occupation_skill_synonyms=None
):
    if occupation_skill_synonyms is None:
        occupation_skill_synonyms = {}

    skill_gap = calculate_skill_gap(
        user_skills,
        required_skills,
        occupation_skill_synonyms
    )

    compatibility = calculate_compatibility_score(
        skill_gap["match_percentage"],
        education_match,
        experience_match,
        interest_match
    )

    return {
        "occupation": occupation,
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "match_percentage": skill_gap["match_percentage"],
        "compatibility_score": compatibility
    }


def rank_occupations(
    user_skills,
    occupations,
    education="",
    experience="",
    interests=None,
    career_goal=""
):
    if interests is None:
        interests = []

    results = []

    for occupation in occupations:

        education_match = calculate_education_match(
            education,
            occupation.get("education_requirements", [])
        )

        experience_match = calculate_experience_match(
            experience,
            occupation.get("experience_level", "")
        )

        interest_match = calculate_interest_match(
            interests,
            occupation["name"]
        )

        career_goal_match = calculate_career_goal_match(
            career_goal,
            occupation["name"]
        )

        result = match_occupation(
            user_skills,
            occupation["name"],
            occupation["required_skills"],
            education_match,
            experience_match,
            interest_match,
            occupation.get("skill_synonyms", {})
        )

        result["career_goal_match"] = career_goal_match

        results.append(result)

    results.sort(
        key=lambda x: (
            x["career_goal_match"],
            x["compatibility_score"]
        ),
        reverse=True
    )

    return results