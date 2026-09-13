def recommend_training(occupation_result, occupations):
    occupation_name = occupation_result["occupation"]
    missing_skills = occupation_result["missing_skills"]

    for occupation in occupations:
        if occupation["name"] == occupation_name:

            recommendations = []

            for training in occupation["training"]:
                recommendations.append({
                    "training": training,
                    "nsqf_level": occupation["nsqf_level"]
                })

            return {
                "occupation": occupation_name,
                "missing_skills": missing_skills,
                "recommendations": recommendations
            }

    return {
        "occupation": occupation_name,
        "missing_skills": missing_skills,
        "recommendations": []
    }