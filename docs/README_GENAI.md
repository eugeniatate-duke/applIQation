# ApplIQation – AI Interview Coach (Generative AI Extension)

Live Application: https://appliqation.vercel.app/

Backend API: https://appliqation-api-428926191821.us-central1.run.app/docs

---

# Overview

ApplIQation extends the existing career readiness platform with a **Generative AI Interview Coach** that produces structured interview preparation using a fine-tuned large language model.

Rather than functioning as a general-purpose chatbot, the Interview Coach transforms structured candidate information—including career readiness, detected technical skill gaps, and personalized learning recommendations—into an interview preparation report.

Developed for **AIPI 540 – Deep Learning Applications** at Duke University.

---

# Project Scope

The Interview Coach is designed for technical careers including:

- Artificial Intelligence
- Machine Learning
- Data Science
- MLOps
- Software Engineering

The system is intended to complement—not replace—the overall career readiness assessment by helping candidates prepare for technical interviews after receiving their readiness prediction and personalized learning recommendations.

---

# Problem

After determining whether a candidate is ready to apply, an important question remains:

> **How should I prepare for the interview?**

The objective of this project was to adapt a pretrained language model to generate interview preparation reports using structured candidate information.

---

# Solution

ApplIQation fine-tunes **FLAN-T5-small** using **LoRA (PEFT)** to generate structured interview preparation reports.

The model receives:

- Career readiness prediction
- Matched technical skills
- Missing technical skills
- Personalized learning recommendations

and generates:

- Overall Assessment
- Highest Priority Skills
- Technical Questions
- Behavioral Questions
- Suggested Study Order

---

# Training Pipeline

```text
Career Readiness Dataset
        │
        ▼
Skill Extraction
        │
        ▼
Recommendation Engine
        │
        ▼
Instruction Dataset (.jsonl)
        │
        ▼
FLAN-T5 + LoRA Fine-Tuning
        │
        ▼
AI Interview Coach
```

---

# Dataset Construction

The supervised instruction dataset was automatically generated from the existing ApplIQation recommendation pipeline.

Each training example contains:

- instruction
- structured candidate profile
- target interview preparation report

Dataset generation is performed by:

```bash
python -m src.genai.build_training_dataset
```

Model training is performed by:

```bash
python -m src.genai.train_lora
```

---

# Model Adaptation

Base Model

```text
google/flan-t5-small
```

Adaptation Strategy

- LoRA
- PEFT
- Seq2SeqTrainer
- Hugging Face Transformers

Only the lightweight LoRA adapter weights are trained while the pretrained FLAN-T5 model remains frozen, enabling efficient fine-tuning and lightweight deployment.

---

# Before vs. After Fine-Tuning

Evaluation compares the pretrained FLAN-T5 model against the LoRA-adapted model using identical candidate inputs.

The pretrained model produces mostly generic interview advice.

After LoRA fine-tuning, the adapted model consistently generates structured interview preparation reports aligned with the desired application format, including prioritized skill gaps, interview questions, and study recommendations.

Evaluation can be reproduced using:

```bash
python -m src.genai.evaluate_flan
```

---

# Evaluation

Evaluation focuses on demonstrating the learned capability rather than reporting traditional language-model benchmarks.

The qualitative comparison examines whether the adapted model learned to:

- generate a consistent interview report structure
- incorporate detected technical skill gaps
- organize interview preparation into logical sections
- recommend an ordered study plan

The evaluation script prints side-by-side outputs from:

- Base FLAN-T5
- Fine-tuned FLAN-T5 + LoRA

using identical candidate inputs.

---

# Risks and Limitations

The instruction-following dataset was generated programmatically from the existing recommendation pipeline and originally synthetically generated data rather than recruiter-authored interview reports.

As a result, the adapted model successfully learns the desired report structure but may produce repetitive interview questions and relatively generic assessments across different job descriptions.

This prototype demonstrates successful model adaptation but should not be considered a production-ready interview coaching system.

Future work would incorporate:

- tech recruiter-authored interview preparation examples
- real interview transcripts
- human evaluation
- company-specific interview data
- Retrieval-Augmented Generation (RAG)

to improve diversity, realism, and personalization.

---

# Deployment

```text
React (Vercel)
        │
        ▼
FastAPI (Google Cloud Run)
        │
        ▼
DistilBERT Career Readiness
        │
        ▼
Recommendation Engine
        │
        ▼
FLAN-T5 LoRA Interview Coach
```

---

# Technologies Used

## Frontend

- React
- Axios
- Vercel

## Backend

- FastAPI
- Google Cloud Run

## Career Readiness

- DistilBERT
- Hugging Face Transformers
- PyTorch

## Generative AI

- FLAN-T5-small
- LoRA
- PEFT
- Seq2SeqTrainer
- Hugging Face Transformers

---

# Future Work

Potential improvements include:

- Recruiter-authored interview coaching datasets
- Real interview transcript fine-tuning
- Role-specific interview question generation
- Human preference evaluation
- Company-specific interview preparation using Retrieval-Augmented Generation (RAG)
- Personalized follow-up interview practice

---

# Author

**Eugenia Tate**

Master of Engineering in Artificial Intelligence

Duke University
