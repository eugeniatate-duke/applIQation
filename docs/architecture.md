# ApplIQation System Architecture

## Overview

ApplIQation is an AI-powered career readiness assessment system that estimates whether a candidate is prepared for a target role.

The system consists of two major pipelines:

1. Synthetic data generation for model training.
2. Production inference for end users.

---

## Training Pipeline

Career Archetype (YAML)

↓

Candidate Generator

↓

Candidate Object

↓

Resume Renderer

↓

Synthetic Resume

+

Job Profile (YAML)

↓

Job Generator

↓

Job Renderer

↓

Synthetic Job Description

↓

Automatic Labeling

↓

Career Readiness Dataset

↓

Model Training

- Naive Baseline
- TF-IDF + Logistic Regression
- DistilBERT


                   TRAINING PIPELINE

 Career YAML                Job YAML
      │                        │
      ▼                        ▼
Candidate Generator      Job Generator
      │                        │
      ▼                        ▼
 Resume Renderer        Job Renderer
      │                        │
      └────────────┬────────────┘
                   ▼
            Automatic Labeling
                   ▼
      Career Readiness Dataset
                   ▼
            Model Training
      (Naive → TF-IDF → DistilBERT)


---

## Production Pipeline

User uploads:

- Resume (PDF, DOCX or TXT)
- Job Description

↓

Resume Parser

↓

Model Inference

↓

LLM Explanation Layer

↓

Outputs

- Readiness Score
- Recommendation
- Competency Gaps
- Assessment Questions
- Learning Roadmap



                  PRODUCTION PIPELINE

 Resume (PDF/DOCX/TXT)
            +
     Job Description
            │
            ▼
      Resume Parser
            ▼
     Trained Classifier
            ▼
     GPT Explanation Layer
            ▼
  Readiness Dashboard

---

## Repository Structure

- Data Generation
- Model Training
- Evaluation
- Backend API
- Frontend Application

---

## Future Enhancements

- Career progression recommendations
- Capability graph
- Personalized learning roadmap
- External market trend integration