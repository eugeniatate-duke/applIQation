"""
generate_candidate.py

Loads a YAML career archetype and generates a synthetic candidate profile.

The returned candidate object is later rendered into a resume and used for automatic labeling.
"""

import random
import uuid
import yaml
from src.data_generation.resume_templates import PROJECT_TOPICS
from src.data_generation.resume_templates import (
    FIRST_NAMES,
    LAST_NAMES
)

def load_profile(profile_path):
    """
    Load a YAML archetype.

    Parameters
    ----------
    profile_path : str

    Returns
    -------
    dict
    """
    with open(profile_path, "r") as f:
        return yaml.safe_load(f)


def generate_candidate(profile):
    """
    Generate a randomized candidate from an archetype.

    Parameters
    ----------
    profile : dict

    Returns
    -------
    dict
    """

    # Randomly choose years of experience
    years = random.randint(
        profile["experience"]["years"]["min"],
        profile["experience"]["years"]["max"]
    )

    # Always include core skills
    skills = list(profile["core_skills"])

    # Randomly sample optional skills
    optional = random.sample(
        profile["optional_skills"],
        random.randint(
            0,
            len(profile["optional_skills"])
        )
    )

    skills.extend(optional)

    # Remove duplicates
    skills = sorted(list(set(skills)))

    # Randomly choose a job title
    # If no titles are defined in the YAML, fall back to the archetype name.
    titles = profile["experience"].get("titles", [profile["name"]])

    title = random.choice(titles)

    # determine project count
    max_projects = min(
        profile["projects"]["max"],
        years + 2
    )

    project_count = random.randint(
        profile["projects"]["min"],
        max_projects
    )

    from src.data_generation.resume_templates import (
        ROLE_PROJECT_TOPICS
    )

    role_projects = ROLE_PROJECT_TOPICS.get(
        profile["name"],
        PROJECT_TOPICS
    )

    projects = random.sample(
        role_projects,
        min(project_count, len(role_projects))
    )

    candidate = {
        "id": str(uuid.uuid4()),
        "name":
            f"{random.choice(FIRST_NAMES)} "
            f"{random.choice(LAST_NAMES)}",
        "role": profile["name"],
        "education": random.choice(
            profile["education"]
        ),
        "experience_years": years,
        "job_title": title,
        "skills": skills,
        "projects": projects
    }

    return candidate 