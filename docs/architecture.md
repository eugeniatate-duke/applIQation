# ApplIQation System Architecture

# Overview

ApplIQation is an AI-powered career readiness platform that combines predictive machine learning, recommendation systems, and generative AI to help candidates evaluate their readiness for technical roles and prepare for interviews.

The platform consists of three integrated components:

1. Career Readiness Classification (DistilBERT)
2. Personalized Learning Recommendation System
3. AI Interview Coach (FLAN-T5 + LoRA)

---

# Training Pipeline

Synthetic Career Profiles (YAML)

↓

Candidate Generator

↓

Resume Renderer

↓

Synthetic Resume

+

Synthetic Job Profiles (YAML)

↓

Job Generator

↓

Job Description Renderer

↓

Automatic Labeling

↓

Career Readiness Dataset

↓

DistilBERT Fine-Tuning

↓

Career Readiness Model

+

Career Readiness Dataset

↓

Skill Extraction

↓

Recommendation Engine

↓

Instruction Dataset Builder

↓

Interview Training Dataset (.jsonl)

↓

FLAN-T5 + LoRA Fine-Tuning

↓

AI Interview Coach Adapter

```
                 TRAINING PIPELINE

 Candidate YAML                 Job YAML
       │                           │
       ▼                           ▼
 Candidate Generator        Job Generator
       │                           │
       ▼                           ▼
 Resume Renderer          Job Renderer
       │                           │
       └──────────────┬────────────┘
                      ▼
             Automatic Labeling
                      ▼
       Career Readiness Dataset
                      │
          ┌───────────┴────────────┐
          ▼                        ▼
 DistilBERT Fine-Tuning      Recommendation Pipeline
          │                        │
          ▼                        ▼
 Career Readiness Model   Interview Training Dataset
                                   │
                                   ▼
                        FLAN-T5 + LoRA Fine-Tuning
                                   │
                                   ▼
                          AI Interview Coach
```

---

# Production Pipeline

User uploads:

- Resume (PDF / DOCX / TXT)
- Target Job Description

↓

Resume Parser

↓

Skill Extraction

↓

DistilBERT Career Readiness Prediction

↓

Gap Analysis

↓

Recommendation Engine

↓

FLAN-T5 LoRA Interview Coach

↓

Career Readiness Dashboard

Outputs:

- Readiness Prediction
- Confidence Score
- Matched Skills
- Missing Skills
- Personalized Learning Recommendations
- AI Interview Preparation Report

```
                 PRODUCTION PIPELINE

 Resume (PDF/DOCX/TXT)
            +
     Job Description
            │
            ▼
      Resume Parser
            │
            ▼
      Skill Extraction
            │
            ▼
 DistilBERT Classifier
            │
            ▼
       Gap Analysis
            │
            ▼
 Recommendation Engine
            │
            ▼
 FLAN-T5 + LoRA Interview Coach
            │
            ▼
      Career Readiness Dashboard
```

---

# Repository Structure

- Synthetic Data Generation
- Career Readiness Dataset
- DistilBERT Training
- Recommendation System
- FLAN-T5 LoRA Training
- Model Evaluation
- Backend API
- React Frontend

---

# Future Enhancements

- Recruiter-authored interview datasets
- Real interview transcript fine-tuning
- Company-specific interview preparation
- Retrieval-Augmented Generation (RAG)
- Personalized learning roadmap
- Labor market trend integration
- Human feedback evaluation
