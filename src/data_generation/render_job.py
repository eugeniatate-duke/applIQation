"""
render_job.py

Render structured job objects into realistic job descriptions.
"""

import random

from src.data_generation.resume_templates import (
    JOB_SUMMARY_TEMPLATES,
    RESPONSIBILITY_TEMPLATES,
    QUALIFICATION_TEMPLATES,
)


def format_skill_list(skills):
    """
    Convert a list of skills into a readable string.
    """
    return ", ".join(skills)


def render_job(job):
    """
    Convert a structured job object into a realistic
    job description.
    """
    lines = []

    # --------------------------------------------------
    # Job Title
    # --------------------------------------------------

    lines.append(job["title"])
    lines.append("")

    # --------------------------------------------------
    # About the Role
    # --------------------------------------------------

    summary = random.choice(
        JOB_SUMMARY_TEMPLATES
    )

    lines.append("ABOUT THE ROLE")
    lines.append(
        summary.format(title=job["title"])
    )
    lines.append("")

    # --------------------------------------------------
    # Responsibilities
    # --------------------------------------------------

    lines.append("RESPONSIBILITIES")
    responsibilities = random.sample(RESPONSIBILITY_TEMPLATES,5)

    for item in responsibilities:
        lines.append(f"• {item}")

    lines.append("")

    # --------------------------------------------------
    # Required Skills
    # --------------------------------------------------

    lines.append("REQUIRED SKILLS")

    for skill in job["required_skills"]:
        lines.append(f"• {skill}")

    lines.append("")

    # --------------------------------------------------
    # Qualifications
    # --------------------------------------------------

    lines.append("QUALIFICATIONS")
    qualifications = random.sample(QUALIFICATION_TEMPLATES,3)

    for item in qualifications:
        lines.append(
            "• " + item.format(
                skills=format_skill_list(
                    random.sample(
                        job["required_skills"],
                        min(3, len(job["required_skills"]))
                    )
                )
            )
        )

    lines.append("")
    lines.append(f"Preferred Education: {job['preferred_education']}")

    lines.append(f"Required Experience: {job['required_experience']}+ years")

    return "\n".join(lines)