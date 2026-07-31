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
from transformers import TrainingArguments
from trl import SFTTrainer
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

OUTPUT_DIR = Path("/content/drive/MyDrive/appliqation/models/career_coach_lora")


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


def build_trainer(
    model,
    tokenizer,
    dataset,
):
    """

    Create supervised fine-tuning trainer.

    """

    training_args = build_training_arguments()

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        processing_class=tokenizer,
        formatting_func=format_example,
        args=training_args,
    )

    return trainer


def load_tokenizer():
    """
    Load tokenizer for the base model.
    """

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
    )

    if tokenizer.pad_token is None:
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


def build_training_arguments():
    """
    Configure supervised fine-tuning.
    """

    return TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=2,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        warmup_ratio=0.05,
        logging_steps=25,
        save_strategy="epoch",
        fp16=True,
        report_to="none",
        remove_unused_columns=True,
    )


def save_adapter(
    trainer,
    tokenizer,
):
    """
    Save trained LoRA adapter.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    trainer.model.save_pretrained(OUTPUT_DIR)

    tokenizer.save_pretrained(OUTPUT_DIR)

    print("\nAdapter saved successfully.")


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

    prompt = (
        f"### Instruction\n\n"
        f"{example['instruction']}\n\n"
        f"### Input\n\n"
        f"Job Title: {example['input']['job_title']}\n"
        f"Readiness: {example['input']['readiness']}\n"
        f"Readiness Score: {example['input']['readiness_score']}\n\n"
        f"Matched Skills:\n{matched}\n\n"
        f"Missing Skills:\n{missing}\n\n"
        f"Recommended Resources:\n{resources}\n\n"
        f"### Response\n\n"
        f"{example['output']}"
    )

    return prompt


if __name__ == "__main__":

    dataset = load_training_dataset()

    print(dataset)

    tokenizer = load_tokenizer()

    print("\nTokenizer loaded successfully.")

    model = load_model()

    # Reduce GPU memory usage
    model.config.use_cache = False

    # Save memory during backpropagation
    model.gradient_checkpointing_enable()

    model = attach_lora(model)

    print("\nLoRA attached successfully.")

    print("\nModel loaded successfully.")

    print("\nPreparing trainer...")

    print("\nColumns:")

    print(dataset.column_names)

    print("\nFirst example:")

    print(dataset[0])

    trainer = build_trainer(
        model,
        tokenizer,
        dataset,
    )
    print("\nTrainer train dataset columns:")
    print(trainer.train_dataset.column_names)

    print("\nTrainer first example:")
    print(trainer.train_dataset[0])

    print("\nStarting training...\n")

    trainer.train()

    print(dataset.column_names)

    print(dataset[0])

    save_adapter(
        trainer,
        tokenizer,
    )

    print("\nTraining complete!")
