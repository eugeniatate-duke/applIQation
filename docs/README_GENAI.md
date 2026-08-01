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

# Model Selection and Adaptation

## Base Model

```text
google/flan-t5-small
```

FLAN-T5-small was selected because it is an instruction-tuned encoder-decoder language model that can efficiently follow structured prompts while remaining lightweight enough for practical deployment.

Compared to an earlier prototype using Qwen2.5-3B, FLAN-T5-small provided a significantly smaller deployment footprint while maintaining the desired interview report generation capability.

## Adaptation Strategy

Rather than fine-tuning all model parameters, the project uses **LoRA (Low-Rank Adaptation)** through the **PEFT** library.

Only lightweight adapter weights are trained while the pretrained FLAN-T5 model remains frozen.

Training was performed using:

- Hugging Face Transformers
- Seq2SeqTrainer
- PEFT
- LoRA

This approach substantially reduces memory requirements, training time, and deployment size while preserving the pretrained language capabilities of FLAN-T5.

---

# Before vs. After Fine-Tuning

Evaluation compares the pretrained FLAN-T5 model against the LoRA-adapted model using identical candidate inputs.

The pretrained model produces mostly generic interview advice.

After LoRA fine-tuning, the adapted model consistently generates structured interview preparation reports aligned with the desired application format, including prioritized skill gaps, interview questions, and study recommendations.
```bash
======================================================================
BASE FLAN-T5
======================================================================
Job Title: Machine Learning Engineer Readiness: Ready with Short Ramp-Up Readiness Score: 77.8 Matched Skills: Python, Docker, RAG, Large Language Models Missing


======================================================================
FLAN-T5 + LORA
======================================================================
INTERVIEW STRATEGY REPORT Overall Assessment Your profile already aligns well with the target role. Focus on strengthening production engineering skills and preparing for technical interviews. Highest Priority Skills - FastAPI - Kubernetes - MLflow Technical Questions - Explain your experience with fastAPI and how it would be used in production ML systems. - Tell me about a production issue you solved. Suggested Study Order
```

![FLAN Eval](/data/flan_eval.png)
**Figure 1.** Qualitative evaluation comparing the pretrained FLAN-T5-small model with the LoRA-adapted Interview Coach. The adapted model consistently produces a structured interview preparation report aligned with the desired output format, whereas the pretrained model generates generic interview advice.

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

The pretrained model produces generic interview advice without following the structured interview-report format expected by the application. After LoRA fine-tuning, the adapted model consistently generates interview preparation reports organized into predefined sections aligned with the application workflow.

---

# Risks and Limitations

# Risks and Limitations

The instruction-following dataset was generated programmatically from the existing recommendation pipeline using an underlying synthetic career-readiness dataset rather than recruiter-authored interview reports.

This accelerated development and enabled rapid prototyping, but it also introduced important limitations.

Because the interview coaching targets were generated from deterministic templates rather than real interview preparation examples, the adapted model learned the desired report structure but also inherited repetitive interview questions and relatively generic assessments.

Furthermore, the qualitative evaluation compares outputs generated from the same synthetic data generation process used during training. Although this demonstrates that the model successfully learned the intended capability, it should not be interpreted as evidence of real-world generalization.

A production-quality system would require evaluation using recruiter-authored interview reports, real candidate profiles, human evaluation, and diverse job descriptions from industry.

This prototype demonstrates successful model adaptation, but not production-ready interview coaching.

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

  Future work would incorporate:

- tech recruiter-authored interview preparation examples
- real interview transcripts
- Role-specific interview question generation
- human evaluation
- company-specific interview data 
- Retrieval-Augmented Generation (RAG)

to improve diversity, realism, and personalization.

---

# Author

**Eugenia Tate**

Master of Engineering in Artificial Intelligence

Duke University
