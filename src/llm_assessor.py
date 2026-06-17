import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LITELLM_TOKEN"),
    base_url="https://litellm.oit.duke.edu/v1"
)


def assess_candidate(
    resume_text,
    job_description,
    target_role="Unknown"
):
    prompt = f"""
You are an expert technical recruiter and hiring manager.

Evaluate a candidate's readiness for a role.

The candidate may be early-career.

Evaluate readiness relative to a realistic entry-level or early-career candidate.

Do not assume senior-level production experience is required unless explicitly stated.

Focus on whether the candidate could reasonably succeed in the role after a short onboarding period.

TARGET ROLE:
{target_role}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Analyze the resume against the job description.

Return ONLY valid JSON.

Required JSON schema:

{{
  "readiness_score": integer,
  "recommendation": "",
  "strengths": [],
  "gaps": [],
  "assessment_questions": []
}}

Rules:

- readiness_score must be 0-100
- recommendation must be one of:
  - Ready Now
  - Ready With Short Ramp-Up
  - Requires Significant Preparation

- strengths should contain 3-5 concise strengths

- gaps should contain 3-5 meaningful missing skills or competency areas

- assessment_questions should contain exactly 5 practical technical questions

- questions should specifically test whether the identified gaps are real

Return JSON only.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except Exception:
        return {
            "readiness_score": 0,
            "recommendation": "Parsing Error",
            "strengths": [],
            "gaps": [],
            "assessment_questions": [
                content
            ]
        }