"""
Prompt templates used by the AI Interview Coach.

These prompts define the behavior we want the fine-tuned
language model to learn.
"""

SYSTEM_PROMPT = """
You are ApplIQation Interview Coach.

Your job is to generate personalized interview preparation
for AI and Machine Learning job seekers.

Always produce:

1. Highest priority technical topics
2. Likely technical interview questions
3. Behavioral interview questions
4. Recommended study order

Your advice should be specific to the candidate's
resume, missing skills, and target position.
"""


def build_prompt(
    readiness,
    matched_skills,
    missing_skills,
    job_description,
):
    """
    Build the prompt that will later be used for both
    training and inference.
    """

    return f"""
Candidate Readiness:
{readiness}

Matched Skills:
{", ".join(matched_skills)}

Missing Skills:
{", ".join(missing_skills)}

Job Description:
{job_description}

Generate personalized interview preparation.
"""
