import random
import yaml

from src.config import KNOWLEDGE_DIR

with open(
    KNOWLEDGE_DIR / "career_progression.yaml",
    "r"
) as f:

    CAREER_MAP = yaml.safe_load(f)


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