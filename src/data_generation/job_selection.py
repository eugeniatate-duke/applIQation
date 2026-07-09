import random
import yaml

from src.config import KNOWLEDGE_DIR

with open(
    KNOWLEDGE_DIR / "career_progression.yaml",
    "r"
) as f:

    CAREER_MAP = yaml.safe_load(f)

JOB_FILES = {
    "AI Engineer": "ai_engineer.yaml",
    "AI Researcher": "ai_researcher.yaml",
    "Backend Engineer": "backend_engineer.yaml",
    "Cloud Engineer": "cloud_engineer.yaml",
    "Data Engineer": "data_engineer.yaml",
    "Data Scientist": "data_scientist.yaml",
    "Junior Software Engineer": "junior_swe.yaml",
    "Machine Learning Engineer": "ml_engineer.yaml",
    "MLOps Engineer": "mlops_engineer.yaml",
    "Senior Software Engineer": "senior_swe.yaml",
}

def choose_job(role):
    """
    Select a target job based on career progression.

    Primary jobs are much more likely than
    secondary or stretch jobs.
    """

    mapping = CAREER_MAP[role]

    choices = (
        mapping["primary_jobs"] * 8
        + mapping["secondary_jobs"] * 2
        + mapping["stretch_jobs"]
    )

    return random.choice(choices)