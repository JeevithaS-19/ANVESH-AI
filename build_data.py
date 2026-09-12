"""
ANVESH AI - Member 5 Knowledge Base Builder
Generates: skills.json, occupations.json, nsqf_training.json,
opportunities.json, beneficiaries_sample.json
Schema is frozen per section 13 of the execution plan.
"""
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1. SKILLS  (skill_id, name, synonyms)
# ---------------------------------------------------------------------------
skills = [
    {"skill_id": "SK001", "name": "Python", "synonyms": ["Python3", "Py"]},
    {"skill_id": "SK002", "name": "Java", "synonyms": ["Core Java", "J2EE"]},
    {"skill_id": "SK003", "name": "JavaScript", "synonyms": ["JS", "ES6"]},
    {"skill_id": "SK004", "name": "HTML", "synonyms": ["HTML5"]},
    {"skill_id": "SK005", "name": "CSS", "synonyms": ["CSS3"]},
    {"skill_id": "SK006", "name": "SQL", "synonyms": ["MySQL", "Structured Query Language"]},
    {"skill_id": "SK007", "name": "Data Structures", "synonyms": ["DSA", "Data Structures and Algorithms"]},
    {"skill_id": "SK008", "name": "REST APIs", "synonyms": ["API Development", "RESTful Services"]},
    {"skill_id": "SK009", "name": "Web Development", "synonyms": ["Web Dev", "Full Stack Development"]},
    {"skill_id": "SK010", "name": "Git/Version Control", "synonyms": ["Git", "GitHub", "Version Control"]},
    {"skill_id": "SK011", "name": "Cloud Basics", "synonyms": ["Cloud Computing", "AWS Basics"]},
    {"skill_id": "SK012", "name": "Excel", "synonyms": ["MS Excel", "Spreadsheets"]},
    {"skill_id": "SK013", "name": "Data Analysis", "synonyms": ["Data Analytics"]},
    {"skill_id": "SK014", "name": "Data Visualization", "synonyms": ["Dashboards", "Power BI", "Tableau"]},
    {"skill_id": "SK015", "name": "Statistics", "synonyms": ["Statistical Analysis"]},
    {"skill_id": "SK016", "name": "Digital Marketing", "synonyms": ["Online Marketing"]},
    {"skill_id": "SK017", "name": "SEO", "synonyms": ["Search Engine Optimization"]},
    {"skill_id": "SK018", "name": "Social Media Marketing", "synonyms": ["SMM"]},
    {"skill_id": "SK019", "name": "Content Writing", "synonyms": ["Copywriting"]},
    {"skill_id": "SK020", "name": "Communication Skills", "synonyms": ["Verbal Communication", "Soft Skills"]},
    {"skill_id": "SK021", "name": "Networking Basics", "synonyms": ["Computer Networking"]},
    {"skill_id": "SK022", "name": "Troubleshooting", "synonyms": ["Technical Troubleshooting"]},
    {"skill_id": "SK023", "name": "Customer Support", "synonyms": ["Customer Service", "Helpdesk"]},
    {"skill_id": "SK024", "name": "UI/UX Design", "synonyms": ["User Experience Design", "Product Design"]},
    {"skill_id": "SK025", "name": "Graphic Design", "synonyms": ["Visual Design"]},
    {"skill_id": "SK026", "name": "Retail Sales", "synonyms": ["Sales Associate Skills", "Point of Sale (POS) Operation"]},
    {"skill_id": "SK027", "name": "Inventory Management", "synonyms": ["Stock Management"]},
    {"skill_id": "SK028", "name": "Cash Handling", "synonyms": ["Billing"]},
    {"skill_id": "SK029", "name": "Electrical Wiring", "synonyms": ["House Wiring", "Domestic Wiring"]},
    {"skill_id": "SK030", "name": "Electrical Safety", "synonyms": ["Safety Compliance"]},
    {"skill_id": "SK031", "name": "Basic Tool Handling", "synonyms": ["Hand Tools", "Power Tools"]},
    {"skill_id": "SK032", "name": "Patient Care Basics", "synonyms": ["Patient Assistance", "Bedside Care"]},
    {"skill_id": "SK033", "name": "First Aid", "synonyms": ["Basic Life Support", "BLS"]},
]

# ---------------------------------------------------------------------------
# 2. OCCUPATIONS  (occupation_id, name, required_skills, education)
# ---------------------------------------------------------------------------
occupations = [
    {
        "occupation_id": "OC001",
        "name": "Software Developer",
        "required_skills": ["SK001", "SK002", "SK007", "SK008", "SK009", "SK010"],
        "education": "Diploma/B.Tech in Computer Science or related field",
        "experience_level": "0-3 years",
    },
    {
        "occupation_id": "OC002",
        "name": "Data Analyst",
        "required_skills": ["SK001", "SK006", "SK012", "SK013", "SK014", "SK015"],
        "education": "Graduate in any discipline; preference for Statistics/CS/Commerce",
        "experience_level": "0-2 years",
    },
    {
        "occupation_id": "OC003",
        "name": "Digital Marketing Executive",
        "required_skills": ["SK016", "SK017", "SK018", "SK019", "SK020"],
        "education": "Graduate in any discipline",
        "experience_level": "0-2 years",
    },
    {
        "occupation_id": "OC004",
        "name": "Web Designer",
        "required_skills": ["SK003", "SK004", "SK005", "SK024", "SK025"],
        "education": "Diploma/Certificate in Web Design or related field",
        "experience_level": "0-2 years",
    },
    {
        "occupation_id": "OC005",
        "name": "IT Support Technician",
        "required_skills": ["SK021", "SK022", "SK023", "SK020"],
        "education": "ITI/Diploma in Computer Science or equivalent NSQF-aligned qualification",
        "experience_level": "0-1 years",
    },
    {
        "occupation_id": "OC006",
        "name": "Retail Sales Associate",
        "required_skills": ["SK026", "SK027", "SK028", "SK020"],
        "education": "10th/12th Pass",
        "experience_level": "0-1 years",
    },
    {
        "occupation_id": "OC007",
        "name": "Domestic Electrician",
        "required_skills": ["SK029", "SK030", "SK031"],
        "education": "ITI in Electrical or NSQF-aligned vocational training",
        "experience_level": "0-2 years",
    },
    {
        "occupation_id": "OC008",
        "name": "Healthcare Support Worker",
        "required_skills": ["SK032", "SK033", "SK020", "SK023"],
        "education": "12th Pass; NSQF-aligned healthcare certification preferred",
        "experience_level": "0-1 years",
    },
]

# ---------------------------------------------------------------------------
# 3. NSQF / QP / NOS TRAINING RECORDS (record_id, title, level, linked_skills)
# ---------------------------------------------------------------------------
nsqf_training = [
    {
        "record_id": "TR001",
        "title": "IT-ITeS Software Developer - Qualification Pack",
        "level": "NSQF Level 5",
        "provider": "NASSCOM-SSC Affiliated Training Partner",
        "mode": "Classroom + Lab",
        "duration_weeks": 12,
        "linked_skills": ["SK001", "SK002", "SK007", "SK008", "SK009"],
        "linked_occupations": ["OC001"],
    },
    {
        "record_id": "TR002",
        "title": "Data Analytics using Python - Skill Certification",
        "level": "NSQF Level 5",
        "provider": "NASSCOM-SSC Affiliated Training Partner",
        "mode": "Online + Lab",
        "duration_weeks": 10,
        "linked_skills": ["SK001", "SK006", "SK013", "SK014", "SK015"],
        "linked_occupations": ["OC002"],
    },
    {
        "record_id": "TR003",
        "title": "Digital Marketing Executive - National Occupational Standard",
        "level": "NSQF Level 4",
        "provider": "Retailers Association Skill Council (RASCI)",
        "mode": "Classroom",
        "duration_weeks": 8,
        "linked_skills": ["SK016", "SK017", "SK018", "SK019"],
        "linked_occupations": ["OC003"],
    },
    {
        "record_id": "TR004",
        "title": "Web Designer - Qualification Pack",
        "level": "NSQF Level 4",
        "provider": "NASSCOM-SSC Affiliated Training Partner",
        "mode": "Classroom + Lab",
        "duration_weeks": 10,
        "linked_skills": ["SK003", "SK004", "SK005", "SK024"],
        "linked_occupations": ["OC004"],
    },
    {
        "record_id": "TR005",
        "title": "IT Helpdesk Attendant - National Occupational Standard",
        "level": "NSQF Level 3",
        "provider": "NASSCOM-SSC Affiliated Training Partner",
        "mode": "Classroom",
        "duration_weeks": 6,
        "linked_skills": ["SK021", "SK022", "SK023"],
        "linked_occupations": ["OC005"],
    },
    {
        "record_id": "TR006",
        "title": "Foundational REST API Development - Skill Add-on",
        "level": "NSQF Level 5",
        "provider": "NASSCOM-SSC Affiliated Training Partner",
        "mode": "Online",
        "duration_weeks": 3,
        "linked_skills": ["SK008", "SK010"],
        "linked_occupations": ["OC001"],
    },
    {
        "record_id": "TR007",
        "title": "Cloud Computing Fundamentals - Skill Add-on",
        "level": "NSQF Level 5",
        "provider": "NASSCOM-SSC Affiliated Training Partner",
        "mode": "Online",
        "duration_weeks": 2,
        "linked_skills": ["SK011"],
        "linked_occupations": ["OC001", "OC002"],
    },
    {
        "record_id": "TR008",
        "title": "Retail Sales Associate - Qualification Pack",
        "level": "NSQF Level 2",
        "provider": "Retailers Association Skill Council (RASCI)",
        "mode": "Classroom + On-the-job",
        "duration_weeks": 6,
        "linked_skills": ["SK026", "SK027", "SK028", "SK020"],
        "linked_occupations": ["OC006"],
    },
    {
        "record_id": "TR009",
        "title": "Electrician (Domestic) - Qualification Pack",
        "level": "NSQF Level 3",
        "provider": "Power Sector Skill Council",
        "mode": "Classroom + Workshop",
        "duration_weeks": 12,
        "linked_skills": ["SK029", "SK030", "SK031"],
        "linked_occupations": ["OC007"],
    },
    {
        "record_id": "TR010",
        "title": "General Duty Assistant (Healthcare) - National Occupational Standard",
        "level": "NSQF Level 4",
        "provider": "Healthcare Sector Skill Council",
        "mode": "Classroom + Clinical Practicum",
        "duration_weeks": 16,
        "linked_skills": ["SK032", "SK033", "SK020", "SK023"],
        "linked_occupations": ["OC008"],
    },
]

# ---------------------------------------------------------------------------
# 4. OPPORTUNITIES (opportunity_id, type, title, location, linked_occupation)
# ---------------------------------------------------------------------------
opportunities = [
    {"opportunity_id": "OP001", "type": "Training", "title": "NSQF Software Developer Bootcamp - Bangalore Skill Center", "location": "Bangalore", "linked_occupation": "OC001"},
    {"opportunity_id": "OP002", "type": "Employment", "title": "Junior Software Developer - Local IT Services Firm", "location": "Bangalore", "linked_occupation": "OC001"},
    {"opportunity_id": "OP003", "type": "Livelihood", "title": "Freelance Web/App Development Gigs - Remote", "location": "Remote", "linked_occupation": "OC001"},
    {"opportunity_id": "OP004", "type": "Training", "title": "Data Analytics Certification Program - Kochi Skill Center", "location": "Kochi", "linked_occupation": "OC002"},
    {"opportunity_id": "OP005", "type": "Employment", "title": "Data Analyst Trainee - Regional Analytics Firm", "location": "Kochi", "linked_occupation": "OC002"},
    {"opportunity_id": "OP006", "type": "Training", "title": "Digital Marketing Skill Certification - Hyderabad Center", "location": "Hyderabad", "linked_occupation": "OC003"},
    {"opportunity_id": "OP007", "type": "Livelihood", "title": "Freelance Social Media Management - Remote", "location": "Remote", "linked_occupation": "OC003"},
    {"opportunity_id": "OP008", "type": "Training", "title": "Web Designer NSQF Program - Ernakulam Skill Center", "location": "Ernakulam", "linked_occupation": "OC004"},
    {"opportunity_id": "OP009", "type": "Employment", "title": "Junior Web Designer - Local Design Studio", "location": "Ernakulam", "linked_occupation": "OC004"},
    {"opportunity_id": "OP010", "type": "Employment", "title": "IT Helpdesk Technician - Regional Service Provider", "location": "Bangalore", "linked_occupation": "OC005"},
    {"opportunity_id": "OP011", "type": "Training", "title": "IT Helpdesk NSQF Certification - Community Skill Center", "location": "Kochi", "linked_occupation": "OC005"},
    {"opportunity_id": "OP012", "type": "Training", "title": "Retail Sales Associate NSQF Program - Chennai Skill Center", "location": "Chennai", "linked_occupation": "OC006"},
    {"opportunity_id": "OP013", "type": "Employment", "title": "Sales Associate - Regional Retail Chain", "location": "Chennai", "linked_occupation": "OC006"},
    {"opportunity_id": "OP014", "type": "Training", "title": "Domestic Electrician NSQF Program - Coimbatore ITI", "location": "Coimbatore", "linked_occupation": "OC007"},
    {"opportunity_id": "OP015", "type": "Livelihood", "title": "Self-Employed Electrician Registration - District Skill Mission", "location": "Coimbatore", "linked_occupation": "OC007"},
    {"opportunity_id": "OP016", "type": "Training", "title": "General Duty Assistant NSQF Program - Mysuru Health Skill Center", "location": "Mysuru", "linked_occupation": "OC008"},
    {"opportunity_id": "OP017", "type": "Employment", "title": "General Duty Assistant - District Hospital", "location": "Mysuru", "linked_occupation": "OC008"},
]

# ---------------------------------------------------------------------------
# 5. SAMPLE BENEFICIARY PROFILES (matches M2->M4 contract fields)
# ---------------------------------------------------------------------------
beneficiaries_sample = [
    {
        "profile_id": "BEN001",
        "name": "Ravi",
        "education": "B.Tech",
        "skills": ["Python", "Java", "Web Development"],
        "experience": 2,
        "location": "Bangalore",
        "career_goal": "Software Development",
        "job_preference": "hybrid",
        "expected_top_match": "OC001",
    },
    {
        "profile_id": "BEN002",
        "name": "Anjali",
        "education": "B.Com",
        "skills": ["Excel", "SQL", "Statistics"],
        "experience": 1,
        "location": "Kochi",
        "career_goal": "Data Analysis",
        "job_preference": "remote",
        "expected_top_match": "OC002",
    },
    {
        "profile_id": "BEN003",
        "name": "Farhan",
        "education": "12th Pass",
        "skills": ["Content Writing", "Social Media Marketing"],
        "experience": 0,
        "location": "Hyderabad",
        "career_goal": "Digital Marketing",
        "job_preference": "onsite",
        "expected_top_match": "OC003",
    },
    {
        "profile_id": "BEN004",
        "name": "Meera",
        "education": "Diploma",
        "skills": ["HTML", "CSS", "Graphic Design"],
        "experience": 1,
        "location": "Ernakulam",
        "career_goal": "Web Design",
        "job_preference": "hybrid",
        "expected_top_match": "OC004",
    },
    {
        "profile_id": "BEN005",
        "name": "Suresh",
        "education": "ITI",
        "skills": ["Networking Basics", "Customer Support"],
        "experience": 0,
        "location": "Bangalore",
        "career_goal": "IT Support",
        "job_preference": "onsite",
        "expected_top_match": "OC005",
    },
    {
        "profile_id": "BEN006",
        "name": "Lakshmi",
        "education": "12th Pass",
        "skills": ["Retail Sales", "Cash Handling"],
        "experience": 1,
        "location": "Chennai",
        "career_goal": "Retail",
        "job_preference": "onsite",
        "expected_top_match": "OC006",
    },
    {
        "profile_id": "BEN007",
        "name": "Karthik",
        "education": "ITI",
        "skills": ["Electrical Wiring", "Basic Tool Handling"],
        "experience": 2,
        "location": "Coimbatore",
        "career_goal": "Electrician",
        "job_preference": "onsite",
        "expected_top_match": "OC007",
    },
    {
        "profile_id": "BEN008",
        "name": "Divya",
        "education": "12th Pass",
        "skills": ["Patient Care Basics", "First Aid"],
        "experience": 0,
        "location": "Mysuru",
        "career_goal": "Healthcare Support",
        "job_preference": "onsite",
        "expected_top_match": "OC008",
    },
]

DATASETS = {
    "skills.json": skills,
    "occupations.json": occupations,
    "nsqf_training.json": nsqf_training,
    "opportunities.json": opportunities,
    "beneficiaries_sample.json": beneficiaries_sample,
}

for filename, data in DATASETS.items():
    path = os.path.join(OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"wrote {filename} ({len(data)} records)")
