def generate_explanation(result):
    occupation = result["occupation"]
    score = result["compatibility_score"]
    matched = result["matched_skills"]
    missing = result["missing_skills"]

    explanation = f"{occupation} is recommended with a compatibility score of {score}%."

    if matched:
        explanation += f" Your matching skills include {', '.join(matched)}."

    if missing:
        explanation += f" You need to develop {', '.join(missing)} to improve your suitability."

    else:
        explanation += " You already have all the required skills."

    return explanation