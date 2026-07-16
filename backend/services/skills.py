"""
skills.py

Extract canonical technical skills from text using a configurable
JSON skills dictionary.
"""

import json
from pathlib import Path

SKILLS_PATH = Path("data/resources/skills_dictionary.json")

with open(SKILLS_PATH, "r") as file:
    CANONICAL_SKILLS = json.load(file)


def extract_skills(text):
    """
    Extract canonical skills from text.

    Parameters
    ----------
    text : str

    Returns
    -------
    list[str]
        Sorted list of canonical skill names.
    """

    text = text.lower()

    found = set()

    for canonical_skill, metadata in CANONICAL_SKILLS.items():

        aliases = metadata["aliases"]

        for alias in aliases:

            if alias.lower() in text:
                found.add(canonical_skill)
                break

    return sorted(found)
