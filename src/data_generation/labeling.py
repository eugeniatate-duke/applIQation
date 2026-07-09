"""
labeling.py

Creates ground-truth readiness labels for synthetic resume-job pairs.

Labels are generated automatically using a weighted scoring
approach based on skill overlap, experience, and education.
"""

from typing import Dict


def calculate_skill_score(candidate: Dict, job: Dict) -> float:
    """
    Calculate the percentage of required job skills
    present in the candidate profile.

    Returns
    -------
    float
        Score between 0 and 100.
    """

    candidate_skills = set(candidate["skills"])
    required_skills = set(job["required_skills"])

    if len(required_skills) == 0:
        return 0

    overlap = len(candidate_skills.intersection(required_skills))

    return (overlap / len(required_skills)) * 100


def calculate_experience_score(candidate: Dict, job: Dict) -> float:
    """
    Compare candidate experience with job requirements.

    If the candidate meets or exceeds the required
    years of experience, they receive full credit.
    """

    candidate_years = candidate["experience_years"]
    required_years = job["required_experience"]

    if candidate_years >= required_years:
        return 100

    return (candidate_years / required_years) * 100


def calculate_education_score(candidate: Dict, job: Dict) -> float:
    """
    Compare education requirements.

    Simple binary scoring for the prototype.
    """

    if candidate["education"] == job["preferred_education"]:
        return 100

    return 50


def calculate_readiness(candidate: Dict, job: Dict):
    """
    Compute the overall readiness score.

    Skills contribute the largest weight because
    they are the strongest indicator of candidate fit.
    """

    skill_score = calculate_skill_score(candidate, job)
    experience_score = calculate_experience_score(candidate, job)
    education_score = calculate_education_score(candidate, job)
    readiness_score = (
        skill_score * 0.70 + experience_score * 0.20 + education_score * 0.10
    )

    if readiness_score >= 80:
        label = "Ready"

    elif readiness_score >= 60:
        label = "Ready with Short Ramp-Up"

    else:
        label = "Requires Significant Preparation"

    return {
        "score": round(readiness_score, 1),
        "label": label,
        "skill_score": round(skill_score, 1),
        "experience_score": round(experience_score, 1),
        "education_score": round(education_score, 1)
    }
