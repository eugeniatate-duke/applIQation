"""
career_coach.py

Load the fine-tuned LoRA Career Coach
and generate personalized interview
preparation.
"""

from pathlib import Path

import torch

from peft import PeftModel

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

BASE_MODEL = "google/flan-t5-small"

ADAPTER_DIR = Path("models/career_coach_lora_flan")

# -----------------------------------------------------
# Load tokenizer
# -----------------------------------------------------

tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL,
)

# -----------------------------------------------------
# Load base model
# -----------------------------------------------------

# if torch.cuda.is_available():

#     DEVICE = "cuda"

#     DTYPE = torch.float16

# elif torch.backends.mps.is_available():

#     DEVICE = "mps"

#     DTYPE = torch.float32

# else:

#     DEVICE = "cpu"

#     DTYPE = torch.float32

base_model = AutoModelForSeq2SeqLM.from_pretrained(
    BASE_MODEL,
)

# base_model.to(DEVICE)

# -----------------------------------------------------
# Load LoRA adapter
# -----------------------------------------------------

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_DIR,
)

# model.to(DEVICE)

model.eval()
# print(f"Career Coach loaded on {DEVICE}")


def build_prompt(
    readiness,
    matched_skills,
    missing_skills,
    recommended_resources,
):
    """
    Build prompt for the AI Career Coach.
    """

    resources = "\n".join(
        [f"- {resource['title']}" for resource in recommended_resources]
    )

    return f"""
### Instruction

Generate personalized interview preparation for this AI job candidate.

### Input

Readiness:
{readiness}

Matched Skills:
{", ".join(matched_skills)}

Missing Skills:
{", ".join(missing_skills)}

Recommended Resources:

{resources}

Generate the interview strategy report.
"""


def generate_interview_report(
    readiness,
    matched_skills,
    missing_skills,
    recommended_resources,
):
    """
    Generate interview preparation.
    """

    prompt = build_prompt(
        readiness,
        matched_skills,
        missing_skills,
        recommended_resources,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
    )

    with torch.inference_mode():
      outputs = model.generate(
          **inputs,
          max_new_tokens=250,
          num_beams=4,
          no_repeat_ngram_size=3,
      )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )

    response = response.replace(" Overall Assessment", "\n\nOverall Assessment")
    response = response.replace(" Highest Priority Skills", "\n\nHighest Priority Skills")
    response = response.replace(" Technical Questions", "\n\nTechnical Questions")
    response = response.replace(" Behavioral Questions", "\n\nBehavioral Questions")
    response = response.replace(" Suggested Study Order", "\n\nSuggested Study Order")
    response = response.replace(" 1. ", "\n\n1. ")
    response = response.replace(" 2. ", "\n2. ")
    response = response.replace(" 3. ", "\n3. ")
    response = response.replace(" 4. ", "\n4. ")
    response = response.replace(" 5. ", "\n5. ")

    response = response.replace(" - ", "\n- ")
    # if "### Instruction" in response:
    #     response = response.split("### Instruction")[0].strip()

    return response


if __name__ == "__main__":

    result = generate_interview_report(
        readiness="Ready",
        matched_skills=[
            "Python",
            "PyTorch",
        ],
        missing_skills=[
            "Docker",
            "FastAPI",
        ],
        recommended_resources=[
            {
                "title": "Docker Guide",
            },
            {
                "title": "FastAPI Docs",
            },
        ],
    )

    print(result)
