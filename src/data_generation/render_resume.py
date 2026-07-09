"""
render_resume.py

Converts a structured candidate object into a synthetic resume.

The generated resumes are used to create training data for the
machine learning models while remaining realistic enough to
simulate resumes encountered in industry.
"""

import random
from pathlib import Path

from src.data_generation.resume_templates import (
    SUMMARY_TEMPLATES,
    EXPERIENCE_TEMPLATES,
    PROJECT_TEMPLATES,
    CERTIFICATIONS,
    PUBLICATIONS
)


def format_skill_list(skills):
    """
    Convert a list of skills into a readable string.

    ["Python", "PyTorch", "Docker"]

    becomes
        "Python, PyTorch, Docker"
    """
    return ", ".join(skills)


def article(word):
    """
    Return the correct indefinite article ("a" or "an")
    for a given word.
    """
    if word.lower().startswith(("a", "e", "i", "o", "u")):
        return "an"
    return "a"


def render_summary(candidate):
    """
    Generate the professional summary section.

    A random template is selected to introduce variation
    across generated resumes.
    """
    template = random.choice(SUMMARY_TEMPLATES)

    return template.format(
        role=candidate["role"],
        years=candidate["experience_years"],
        skills=format_skill_list(candidate["skills"][:3])
    )


def render_skills(candidate):
    """
    Render the technical skills section.
    Randomly hide some skills so that the models
    must infer capabilities from resume context.
    """
    visible_skill_count = max(3,int(len(candidate["skills"]) * 0.7))

    visible_skills = random.sample(
        candidate["skills"],
        visible_skill_count
    )

    return " • ".join(sorted(visible_skills))


def render_experience(candidate):
    """
    Generate several realistic experience bullet points.

    A subset of templates is randomly selected to
    increase resume diversity.
    """

    bullets = []

    # Select three unique experience templates
    selected = random.sample(EXPERIENCE_TEMPLATES, 3)

    for template in selected:
        bullets.append(
            template.format(
                skills=format_skill_list(
                    random.sample(
                        candidate["skills"],
                        min(3, len(candidate["skills"]))
                    )
                )
            )
        )
    return bullets


def render_projects(candidate):
    """
    Generate project descriptions.

    Each project receives one randomly selected template
    populated with a random subset of candidate skills.
    """

    project_lines = []

    for project in candidate["projects"]:
        template = random.choice(PROJECT_TEMPLATES)
        description = template.format(
            article=article(project),
            project=project,
            skills=format_skill_list(
                random.sample(
                    candidate["skills"],
                    min(3, len(candidate["skills"]))
                )
            )
        )

        project_lines.append(
            {
                "title": project,
                "description": description
            }
        )
    return project_lines


def render_resume(candidate):
    """
    Convert a candidate object into resume text.

    Returns
    -------
    str
        Formatted resume.
    """

    summary = render_summary(candidate)
    skills = render_skills(candidate)
    experience = render_experience(candidate)
    projects = render_projects(candidate)
    lines = []

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    lines.append(candidate["name"])
    lines.append("")

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    lines.append("PROFESSIONAL SUMMARY")
    lines.append(summary)
    lines.append("")

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    lines.append("EDUCATION")
    lines.append(candidate["education"])
    lines.append("")

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    lines.append("TECHNICAL SKILLS")
    lines.append(skills)
    lines.append("")

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    lines.append("PROFESSIONAL EXPERIENCE")
    lines.append(
        f"{candidate['job_title']} "
        f"({candidate['experience_years']} years)"
    )

    for bullet in experience:
        lines.append(f"• {bullet}")

    lines.append("")

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    lines.append("PROJECTS")

    for project in projects:
        lines.append(project["title"])
        lines.append(
            f"• {project['description']}"
        )
        lines.append("")

    if candidate["role"] in CERTIFICATIONS:
        lines.append("")
        lines.append("CERTIFICATIONS")

        for cert in CERTIFICATIONS[candidate["role"]]:
            lines.append(f"• {cert}")

    if candidate["role"] in PUBLICATIONS:
        lines.append("")
        lines.append("PUBLICATIONS")

        publication = random.choice(
            PUBLICATIONS[candidate["role"]]
        )

        lines.append(f"• {publication}")

    return "\n".join(lines)


def save_resume(resume_text, candidate, output_directory):
    """
    Save a generated resume to disk.

    Parameters
    ----------
    resume_text : str
    candidate : dict
    output_directory : Path
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    role = (
        candidate["role"]
        .lower()
        .replace(" ", "_")
    )

    filename = (
        output_directory
        / f"{role}_{candidate['id']}.txt"
    )

    # filename = output_directory / f"{candidate['id']}.txt"

    with open(filename, "w") as f:
        f.write(resume_text)