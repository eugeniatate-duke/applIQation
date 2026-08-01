"""
evaluate_flan.py

Qualitative evaluation of the fine-tuned
FLAN-T5 Career Coach.

Compares the pretrained FLAN model against
the LoRA-adapted model using the same
candidate profile.
"""

from pathlib import Path

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

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)


# -----------------------------------------------------
# Prompt
# -----------------------------------------------------

PROMPT = """
Generate personalized interview preparation for this technical job candidate.

Job Title:
Machine Learning Engineer

Readiness:
Ready with Short Ramp-Up

Readiness Score:
77.8

Matched Skills:
Python, Docker, RAG, Large Language Models

Missing Skills:
FastAPI, Kubernetes, MLflow

Recommended Resources:

- FastAPI Official Tutorial
- Kubernetes Basics
- MLflow Documentation
"""


def generate(model):
    """
    Generate interview report.
    """

    inputs = tokenizer(
        PROMPT,
        return_tensors="pt",
        truncation=True,
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        num_beams=4,
        no_repeat_ngram_size=3,
    )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )


# -----------------------------------------------------
# Base model
# -----------------------------------------------------

print("=" * 70)
print("BASE FLAN-T5")
print("=" * 70)

base_model = AutoModelForSeq2SeqLM.from_pretrained(
    BASE_MODEL,
)

print(generate(base_model))


# -----------------------------------------------------
# Fine-tuned model
# -----------------------------------------------------

print("\n")
print("=" * 70)
print("FLAN-T5 + LORA")
print("=" * 70)

adapted_model = PeftModel.from_pretrained(
    AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL),
    ADAPTER_DIR,
)

print(generate(adapted_model))
