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
    AutoModelForCausalLM,
    AutoTokenizer,
)

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"

ADAPTER_DIR = Path("models/career_coach_lora")

# -----------------------------------------------------
# Load tokenizer
# -----------------------------------------------------

tokenizer = AutoTokenizer.from_pretrained(
    ADAPTER_DIR,
)

# -----------------------------------------------------
# Load base model
# -----------------------------------------------------

if torch.cuda.is_available():

    DEVICE = "cuda"

    DTYPE = torch.float16

elif torch.backends.mps.is_available():

    DEVICE = "mps"

    DTYPE = torch.float32

else:

    DEVICE = "cpu"

    DTYPE = torch.float32

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    dtype=DTYPE,
)

base_model.to(DEVICE)

# -----------------------------------------------------
# Load LoRA adapter
# -----------------------------------------------------

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_DIR,
)

model.to(DEVICE)

model.eval()
print(f"Career Coach loaded on {DEVICE}")


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

### Response
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
    )

    inputs = {
        k: v.to(DEVICE)
        for k, v in inputs.items()
    }

    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        temperature=0.6,
        top_p=0.9,
        use_cache=True,
        repetition_penalty=1.1,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1] :]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    if "### Instruction" in response:
        response = response.split("### Instruction")[0].strip()

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
