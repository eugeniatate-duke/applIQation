"""
train_lora.py

Fine-tune the ApplIQation AI Career Coach
using LoRA.

This script trains an instruction-following
language model on the interview coaching
dataset generated from the existing
ApplIQation pipeline.
"""

from pathlib import Path
from transformers import AutoModelForCausalLM
from datasets import load_dataset
from transformers import AutoTokenizer
from peft import (
    LoraConfig,
    get_peft_model,
)

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

DATASET_PATH = "data/genai/interview_training.jsonl"

OUTPUT_DIR = Path("models/career_coach_lora")


def load_training_dataset():
    """
    Load the JSONL instruction dataset.
    """

    dataset = load_dataset(
        "json",
        data_files=DATASET_PATH,
        split="train",
    )

    return dataset


def load_tokenizer():
    """
    Load tokenizer for the base model.
    """

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
    )

    tokenizer.pad_token = tokenizer.eos_token

    return tokenizer

def load_model():
    """
    Load the base instruction model.
    """

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
    )

    return model

def attach_lora(model):
    """
    Attach LoRA adapters to the base model.
    """

    config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",

        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
        ],
    )

    model = get_peft_model(
        model,
        config,
    )

    model.print_trainable_parameters()

    return model

def format_example(example):
    """
    Convert one structured training example into
    an instruction-tuning prompt.
    """

    resources = "\n".join(
        [
            f"- {r['title']} ({r['priority']})"
            for r in example["input"]["recommended_resources"]
        ]
    )

    matched = ", ".join(example["input"]["matched_skills"])

    missing = ", ".join(example["input"]["missing_skills"])

    prompt = f"""### Instruction

    {example["instruction"]}

    ### Input

    Job Title:
    {example["input"]["job_title"]}

    Readiness:
    {example["input"]["readiness"]}

    Readiness Score:
    {example["input"]["readiness_score"]}

    Matched Skills:
    {matched}

    Missing Skills:
    {missing}

    Recommended Resources:

    {resources}

    ### Response

    {example["output"]}
    """

    return {
          "text": prompt
    }


if __name__ == "__main__":

    dataset = load_training_dataset()

    dataset = dataset.map(

        format_example

    )

    print(dataset)

    tokenizer = load_tokenizer()

    print("\nTokenizer loaded successfully.")

    model = load_model()

    model = attach_lora(model)

    print("\nLoRA attached successfully.")

    print("\nModel loaded successfully.")

    print("\nFirst example:\n")

    print(dataset[0]["text"])
