"""
dataset_generator.py

Generate synthetic instruction-response examples
for fine-tuning the AI Interview Coach.

These examples teach the model how to generate
personalized interview preparation.
"""

import json
import random
from pathlib import Path

OUTPUT_FILE = Path("data/genai/interview_training.jsonl")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------
# Example skill pools
# -----------------------------------------------------

COMMON_SKILLS = [
    "Python",
    "SQL",
    "Docker",
    "AWS",
    "Kubernetes",
    "FastAPI",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "CI/CD",
    "Git",
    "Linux",
    "MLflow",
    "Airflow",
    "Spark",
]

JOB_TITLES = [
    "Machine Learning Engineer",
    "AI Engineer",
    "Data Scientist",
    "ML Platform Engineer",
]


READINESS = [
    "Ready",
    "Ready with Short Ramp-Up",
    "Requires Significant Preparation",
]


def sample_candidate():
    """
    Generate one synthetic candidate profile.
    """

    matched = random.sample(COMMON_SKILLS, k=5)
    remaining = list(set(COMMON_SKILLS) - set(matched))
    missing = random.sample(remaining, k=4)

    return {
        "matched": matched,
        "missing": missing,
        "job": random.choice(JOB_TITLES),
        "readiness": random.choice(READINESS),
    }


def generate_response(candidate):
    """
    Create the desired Interview Coach output.

    This becomes the supervised target for LoRA.
    """

    highest = candidate["missing"][:2]
    response = f"""
INTERVIEW PREPARATION

Highest Priority Topics

- {highest[0]}
- {highest[1]}

Likely Technical Interview Questions

1. Explain how you have used {highest[0]} in production.

2. Describe challenges when deploying ML systems with {highest[1]}.

Behavioral Questions

- Describe a difficult ML project.

- Tell me about a production issue you solved.

Recommended Study Order

1. {candidate["missing"][0]}
2. {candidate["missing"][1]}
3. {candidate["missing"][2]}
4. {candidate["missing"][3]}
"""

    return response.strip()

# -----------------------------------------------------
# Generate training dataset
# -----------------------------------------------------


def generate_dataset(num_examples=500):
    """
    Generate a JSONL dataset for LoRA fine-tuning.
    """

    with open(OUTPUT_FILE, "w") as f:

        for _ in range(num_examples):

            candidate = sample_candidate()

            example = {
                "instruction": (
                    "Generate personalized interview preparation for "
                    "this AI job candidate."
                ),
                "input": {
                    "readiness": candidate["readiness"],
                    "matched_skills": candidate["matched"],
                    "missing_skills": candidate["missing"],
                    "job_title": candidate["job"],
                },
                "output": generate_response(candidate),
            }

            f.write(json.dumps(example) + "\n")

    print(f"\nGenerated {num_examples} training examples.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_dataset(num_examples=500)
