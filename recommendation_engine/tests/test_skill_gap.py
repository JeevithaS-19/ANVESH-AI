from recommendation_engine.skill_gap import calculate_skill_gap
user_skills = ["Python", "SQL", "Java"]

required_skills = ["Python", "SQL", "Machine Learning", "Statistics"]

result = calculate_skill_gap(user_skills, required_skills)
print(result)