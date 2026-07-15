"""
resource_recommender.py

Content-based learning resource recommender for ApplIQation.
"""

import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RESOURCE_PATH = Path("data/resources/learning_resources.json")


def load_resources(resource_path=RESOURCE_PATH):
    with open(resource_path, "r") as file:
        return json.load(file)


def resource_to_text(resource):
    return " ".join(
        [
            resource["title"],
            resource["description"],
            " ".join(resource["skills"]),
            resource["category"],
            resource["format"],
            resource["difficulty"],
        ]
    )


def build_user_query(missing_skills, job_description=""):
    if missing_skills:
        return " ".join(missing_skills) + " " + job_description

    return job_description


def recommend_resources(
    missing_skills,
    job_description="",
    top_k=5,
    diversity=True,
):
    """
    Recommend learning resources using content-based filtering.

    The recommender handles the cold-start case because it does not require
    historical clicks, ratings, or user-item interactions. It uses extracted
    skill gaps and job-description context as the user profile.
    """

    resources = load_resources()

    query = build_user_query(
        missing_skills,
        job_description,
    )

    resource_texts = [resource_to_text(resource) for resource in resources]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    matrix = vectorizer.fit_transform([query] + resource_texts)

    query_vector = matrix[0]
    resource_vectors = matrix[1:]

    similarities = cosine_similarity(
        query_vector,
        resource_vectors,
    ).flatten()

    missing_skill_set = set(missing_skills)

    for i, resource in enumerate(resources):
        resource_skills = set(resource["skills"])
        overlap = missing_skill_set.intersection(resource_skills)

        skill_boost = 0.08 * len(overlap)
        similarities[i] += skill_boost

    ranked_indices = np.argsort(similarities)[::-1]

    recommendations = []
    used_formats = set()
    used_categories = set()

    for index in ranked_indices:
        resource = resources[index]
        score = float(similarities[index])

        if score <= 0:
            continue

        if diversity:
            already_same_format = resource["format"] in used_formats
            already_same_category = resource["category"] in used_categories

            if (
                len(recommendations) < top_k - 1
                and already_same_format
                and already_same_category
            ):
                continue

        matched_skills = [
            skill for skill in resource["skills"] if skill in missing_skills
        ]

        if matched_skills:
            reason = (
                "Recommended because it directly addresses: "
                + ", ".join(matched_skills)
                + "."
            )
        else:
            reason = (
                "Recommended because it is semantically related to the target role "
                "and supports broader career preparation."
            )

        recommendation = {
            "id": resource["id"],
            "title": resource["title"],
            "provider": resource["provider"],
            "url": resource["url"],
            "skills": resource["skills"],
            "category": resource["category"],
            "format": resource["format"],
            "difficulty": resource["difficulty"],
            "duration_hours": resource["duration_hours"],
            "score": round(score, 3),
            "reason": reason,
        }

        recommendations.append(recommendation)
        used_formats.add(resource["format"])
        used_categories.add(resource["category"])

        if len(recommendations) == top_k:
            break

    return recommendations


if __name__ == "__main__":
    sample_missing_skills = ["Docker", "AWS", "FastAPI", "MLOps"]

    results = recommend_resources(
        missing_skills=sample_missing_skills,
        job_description="Machine learning engineer role requiring deployment and cloud experience.",
    )

    for item in results:
        print(item["title"], item["score"], item["reason"])
