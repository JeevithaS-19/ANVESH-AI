from recommendation_engine.occupation_matcher import rank_occupations
from recommendation_engine.data.occupations import OCCUPATIONS

user_skills = ["Python", "SQL", "Java"]

results = rank_occupations(user_skills, OCCUPATIONS)

for result in results:
    print(result)