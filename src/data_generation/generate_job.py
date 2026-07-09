"""
generate_job.py

Loads a structured job profile and converts it into job object for labeling and rendering.
"""
import yaml

def load_job_profile(profile_path):
    """
    Load a job profile YAML.

    Parameters
    ----------
    profile_path : Path

    Returns
    -------
    dict
    """
    with open(profile_path, "r") as f:
        return yaml.safe_load(f)


def generate_job(profile):
    """
    Convert a YAML profile into a job object.

    No randomness is required because the
    YAML already represents the desired role.
    """

    return {
        "title": profile["title"],
        "required_skills": profile["required_skills"],

        "required_experience":
            profile["required_experience"],

        "preferred_education":
            profile["preferred_education"]
    }