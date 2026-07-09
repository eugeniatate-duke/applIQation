"""
baseline_model.py

Naive baseline model based on keyword overlap.

The model predicts candidate readiness by comparing
the overlap between resume skills and required job skills.
"""

import pandas as pd


def extract_skills(text):
    """
    Extract skills from a block of text.

    The baseline assumes every bullet under
    'TECHNICAL SKILLS' or 'REQUIRED SKILLS'
    represents a skill.
    """

    skills = []
    capture = False

    for line in text.splitlines():
        line = line.strip()

        if line == "TECHNICAL SKILLS":
            capture = True
            continue

        if line == "REQUIRED SKILLS":
            capture = True
            continue

        if capture:

            # Stop when another section begins.
            if line.isupper() and len(line) > 3:
                break

            # Resume skills are separated by bullets.
            if "•" in line:
                skills.extend(
                    [
                        skill.strip()
                        for skill in line.split("•")
                        if skill.strip()
                    ]
                )

            # Job descriptions use one bullet per line.
            elif line.startswith("•"):
                skills.append(line.replace("•", "").strip())

    return set(skills)


def predict_label(overlap_score):
    """
    Convert overlap percentage into a readiness class.
    """
    if overlap_score >= 80:
        return "Ready"

    if overlap_score >= 60:
        return "Ready with Short Ramp-Up"

    return "Requires Significant Preparation"


def evaluate_baseline(dataset_path):
    """
    Evaluate the naive baseline on the generated dataset.
    """

    df = pd.read_csv(dataset_path)
    predictions = []

    for _, row in df.iterrows():
        resume_skills = extract_skills(
            row["resume_text"]
        )
        job_skills = extract_skills(
            row["job_text"]
        )
        if len(job_skills) == 0:
            overlap = 0
        else:
            overlap = (
                len(resume_skills.intersection(job_skills))/ len(job_skills)) * 100

        predictions.append(predict_label(overlap))

    df["baseline_prediction"] = predictions

    return (
        df,
        df["readiness_label"],
        df["baseline_prediction"]
    )