"""
build_training_dataset.py

Build the supervised fine-tuning dataset for the
ApplIQation AI Career Coach.

This script converts the existing career readiness dataset
into instruction-following examples for LoRA fine-tuning.

Pipeline

career_readiness_dataset.csv

↓

Skill Extraction

↓

Recommendation System

↓

Instruction Dataset (.jsonl)
"""

import json
from pathlib import Path

import pandas as pd

from backend.services.skills import extract_skills
from src.recommender.resource_recommender import recommend_resources

TECHNICAL_SKILLS = {
    "Python",
    "SQL",
    "Docker",
    "AWS",
    "FastAPI",
    "PyTorch",
    "TensorFlow",
    "Transformers",
    "Machine Learning",
    "Deep Learning",
    "Scikit-learn",
    "MLflow",
    "Spark",
    "Airflow",
    "Linux",
    "Git",
    "Kubernetes",
    "REST APIs",
    "MLOps",
    "Backend Development",
}

SOFT_SKILLS = {
    "Communication",
    "Leadership",
    "Teamwork",
    "UI/UX",
    "Agile",
}

# -----------------------------------------------------
# Paths
# -----------------------------------------------------

INPUT_DATASET = Path("data/processed/career_readiness_dataset.csv")

OUTPUT_DATASET = Path("data/genai/interview_training.jsonl")

OUTPUT_DATASET.parent.mkdir(
    parents=True,
    exist_ok=True,
)


def build_instruction():
    """
    The instruction remains identical for every example.

    The model learns to transform structured candidate
    information into personalized interview coaching.
    """

    return "Generate personalized interview preparation " "for this AI job candidate."


def build_input(
    row,
    matched_skills,
    missing_skills,
    recommendations,
):
    """
    Build the structured prompt that will later be
    provided to the language model.
    """

    return {
        "job_title": row["job_title"],
        "readiness": row["readiness_label"],
        "readiness_score": row["readiness_score"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommended_resources": recommendations,
    }


def build_output(
    row,
    matched_skills,
    missing_skills,
    recommendations,
):
    """
    Create the desired Interview Coach response.

    This becomes the supervised target used
    during LoRA fine-tuning.
    """

    if row["readiness_label"] == "Ready":

        assessment = (
            "Your profile already aligns well with the target role. "
            "Focus on strengthening production engineering skills "
            "and preparing for technical interviews."
        )

    elif row["readiness_label"] == "Ready with Short Ramp-Up":

        assessment = (
            "You are close to being competitive for this role. "
            "Addressing a few targeted technical gaps should "
            "substantially improve your readiness."
        )

    else:

        assessment = (
            "Several important technical competencies are still "
            "missing. Prioritize foundational engineering skills "
            "before interviewing."
        )

    technical_missing = [
        skill
        for skill in missing_skills
        if skill in TECHNICAL_SKILLS
    ]

    behavioral_missing = [
        skill
        for skill in missing_skills
        if skill in SOFT_SKILLS
    ]

    technical_questions = []

    for skill in technical_missing[:3]:

        technical_questions.append(
            f"Explain your experience with {skill} "
            f"and how it would be used in production ML systems."
        )

    behavioral_questions = [
        "Describe a challenging machine learning project.",
        "Tell me about a production issue you solved.",
    ]

    if behavioral_missing:

        behavioral_questions.append(
            f"Describe a situation where you demonstrated {behavioral_missing[0]}."
        )

    study_order = [resource["title"] for resource in recommendations]

    report = f"""
INTERVIEW STRATEGY REPORT

Overall Assessment

{assessment}

Highest Priority Skills

{chr(10).join('- ' + s for s in missing_skills)}

Technical Questions

{chr(10).join('- ' + q for q in technical_questions)}

Behavioral Questions

{chr(10).join('- ' + q for q in behavioral_questions)}

Suggested Study Order

{chr(10).join(f'{i+1}. {r}' for i, r in enumerate(study_order))}
"""

    return report.strip()


def build_training_dataset():
    """
    Convert the existing career readiness dataset into
    supervised instruction-following examples.
    """

    df = pd.read_csv(INPUT_DATASET)

    examples = []

    for _, row in df.iterrows():

        resume_text = row["resume_text"]
        job_text = row["job_text"]

        # -----------------------------------------
        # Existing ApplIQation pipeline
        # -----------------------------------------

        resume_skills = extract_skills(resume_text)

        job_skills = extract_skills(job_text)

        matched_skills = [skill for skill in job_skills if skill in resume_skills]

        missing_skills = [skill for skill in job_skills if skill not in resume_skills]

        recommendations = recommend_resources(
            missing_skills=missing_skills,
            job_description=job_text,
            top_k=3,
        )

        example = {
            "instruction": build_instruction(),
            "input": build_input(
                row,
                matched_skills,
                missing_skills,
                recommendations,
            ),
            "output": build_output(
                row,
                matched_skills,
                missing_skills,
                recommendations,
            ),
        }

        examples.append(example)

    return examples


def save_dataset(examples):
    """
    Save instruction dataset in JSONL format.
    """

    with open(OUTPUT_DATASET, "w") as f:

        for example in examples:

            f.write(json.dumps(example) + "\n")

    print(f"\nSaved {len(examples)} examples")

    print(OUTPUT_DATASET)


if __name__ == "__main__":

    dataset = build_training_dataset()

    save_dataset(dataset)

    print("\nFirst example:\n")

    print(
        json.dumps(
            dataset[0],
            indent=2,
        )
    )
