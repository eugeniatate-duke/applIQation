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
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
)

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

MODEL_NAME = "google/flan-t5-small"

DATASET_PATH = "data/genai/interview_training.jsonl"

OUTPUT_DIR = Path("/content/drive/MyDrive/appliqation/models/career_coach_lora_flan")


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
    Create Seq2Seq trainer.
    """

    dataset = dataset.map(
        tokenize,
        batched=True,
        remove_columns=dataset.column_names,
    )

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
    )

    training_args = build_training_arguments()

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
        processing_class=tokenizer,
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

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME,
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
        task_type=TaskType.SEQ_2_SEQ_LM,
        target_modules=[
            "q",
            "v",
        ],
    )

    model = get_peft_model(
        model,
        config,
    )

    model.print_trainable_parameters()

    return model


def build_training_arguments():

    return Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR),
        learning_rate=2e-4,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=2,
        logging_steps=25,
        eval_strategy="no",
        save_strategy="epoch",
        save_total_limit=1,
        predict_with_generate=True,
        fp16=False,
        report_to=[],
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


def preprocess(example):
    """
    Convert one example into
    source/target pairs for FLAN.
    """

    resources = "\n".join(
        f"- {r['title']} ({r['priority']})"
        for r in example["input"]["recommended_resources"]
    )

    source = (
        f"{example['instruction']}\n\n"
        f"Job Title: {example['input']['job_title']}\n"
        f"Readiness: {example['input']['readiness']}\n"
        f"Readiness Score: {example['input']['readiness_score']}\n\n"
        f"Matched Skills:\n"
        f"{', '.join(example['input']['matched_skills'])}\n\n"
        f"Missing Skills:\n"
        f"{', '.join(example['input']['missing_skills'])}\n\n"
        f"Recommended Resources:\n"
        f"{resources}"
    )

    return {
        "source": source,
        "target": example["output"],
    }


def tokenize(batch):
    """
    Tokenize source and target.
    """

    model_inputs = tokenizer(
        batch["source"],
        max_length=384,
        truncation=True,
    )

    labels = tokenizer(
        text_target=batch["target"],
        max_length=256,
        truncation=True,
    )

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs


if __name__ == "__main__":

    dataset = load_training_dataset()
    dataset = dataset.map(preprocess)

    print(dataset)

    tokenizer = load_tokenizer()
    globals()["tokenizer"] = tokenizer

    print("\nTokenizer loaded successfully.")

    model = load_model()

    model = attach_lora(model)

    print("\nLoRA attached successfully.")

    print("\nModel loaded successfully.")

    print("\nPreparing trainer...")

    trainer = build_trainer(
        model,
        tokenizer,
        dataset,
    )

    print("\nStarting training...\n")

    trainer.train()

    save_adapter(
        trainer,
        tokenizer,
    )

    print("\nTraining complete!")
