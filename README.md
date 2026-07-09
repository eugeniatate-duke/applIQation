
# ApplIQation - Know Before You Apply

Vercel App: https://appliqation.vercel.app/ 

Backend API (Google Cloud Run) : https://appliqation-api-428926191821.us-central1.run.app/docs

### AI-Powered Job Readiness Assessment

ApplIQation is an end-to-end NLP application that evaluates how well a candidate's resume aligns with a target job description. The system combines transformer-based semantic understanding with explicit skill matching to estimate career readiness, identify technical gaps, and generate personalized learning recommendations.

The project demonstrates the complete lifecycle of an applied NLP system, including synthetic data generation, classical and deep learning model development, evaluation, deployment, and a production-style web application built with React and FastAPI.

Developed for **AIPI 540 – Deep Learning Applications** at Duke University.

---

## Problem Statement

Resume screening remains one of the most time-consuming stages of the hiring process. Traditional Applicant Tracking Systems (ATS) frequently rely on keyword matching, making them sensitive to differences in wording and unable to recognize semantically equivalent skills or experiences.

Job seekers face a similar challenge. Many applicants struggle to determine whether they are genuinely prepared for a role or whether they should first strengthen specific technical competencies.

ApplIQation investigates whether transformer-based NLP models can provide more reliable career readiness assessments than traditional keyword-based approaches by jointly analyzing resumes and job descriptions.

---

## Solution

ApplIQation performs an end-to-end career readiness assessment by:

1. Parsing uploaded resumes (PDF, DOCX, TXT)
2. Extracting technical skills from resumes and job descriptions
3. Performing semantic resume-job analysis using a fine-tuned DistilBERT model
4. Identifying matched and missing technical skills
5. Estimating overall career readiness
6. Generating a personalized learning roadmap

Rather than relying solely on keyword overlap, the application combines semantic understanding with explicit skill matching to provide transparent and actionable recommendations.

---

## System Architecture

```text

                Resume
                   +

           Job Description

                   │
                   ▼

        React Frontend (Vercel)

                   │
                   ▼

       FastAPI Backend (Cloud Run)

                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼

Skill Extraction      Fine-tuned DistilBERT

        │                     │
        └──────────┬──────────┘
                   ▼

      Career Readiness Assessment
                   ▼
       Learning Roadmap & Feedback

```

---

## Dataset

A synthetic career readiness dataset was developed specifically for this project.

The pipeline automatically generates:

- Synthetic candidate profiles
- Realistic resumes
- Target job descriptions
- Ground-truth readiness labels

Each synthetic candidate is evaluated against multiple target jobs spanning primary, adjacent, and stretch career paths. This produces resume–job pairs that encourage the model to learn relationships between candidates and specific roles rather than memorizing candidate profiles alone.

Dataset summary:

| Item | Count |
|------|------:|
| Candidate archetypes | 10 |
| Resume–Job pairs | 4,300 |
| Readiness classes | 3 |

--- 

## Modeling Approaches
Three progressively more sophisticated models were implemented.

### Naive Baseline Approach

A majority-class classifier establishes a lower-bound performance benchmark.

### Classical Machine Learning

A TF-IDF vectorizer converts resume–job pairs into sparse feature vectors.

These features are classified using Logistic Regression with balanced class weights.

### Deep Learning

The final production model uses DistilBERT with transfer learning.

Resume–job pairs are tokenized jointly and fine-tuned for three-way sequence classification:

- Ready

- Ready with Short Ramp-Up

- Requires Significant Preparation

The deployed application uses the fine-tuned DistilBERT model together with explicit skill matching to produce interpretable recommendations.

---

## Evaluation

Three modeling approaches were evaluated using the same held-out test set.

Evaluation metrics included:

- Accuracy
- Precision
- Recall
- Macro F1 Score
- Confusion Matrix

### Model Comparison

| Model | Accuracy | Macro F1 |
|--------|---------:|---------:|
| Naive Baseline | 72.0% | 0.348 |
| Logistic Regression | 66.0% | 0.567 |
| DistilBERT | **94.5%** | **0.928** |

The transformer-based model substantially outperformed both the baseline and the classical machine learning approach, demonstrating the benefits of contextual language understanding for resume–job matching.

---

## Example Output

```text
Career Readiness Assessment
Ready with Short Ramp-Up
AI Confidence: 95.1%

Matched Skills

✓ Python
✓ Docker
✓ Machine Learning
✓ FastAPI

Missing Skills
• AWS
• Kubernetes

Personalized Learning Roadmap

• Gain hands-on AWS experience
• Learn Kubernetes fundamentals
• Build one cloud-deployed ML application
```
--- 

## Deployment

The application is deployed as a production-style web application.

```text
React
(Vercel)
        │
        ▼
FastAPI
(Google Cloud Run)
        │
        ▼
Fine-tuned DistilBERT
```

The frontend is hosted on Vercel while the FastAPI backend and DistilBERT model are deployed on Google Cloud Run.

---

## Technologies Used

### Frontend
- React
- Axios
- Vercel

### Backend
- FastAPI
- Uvicorn
- Google Cloud Run

### NLP & Machine Learning
- DistilBERT
- Transformers
- PyTorch
- Scikit-learn
- Hugging Face Datasets

### Data Processing
- Pandas
- NumPy
- pdfplumber
- python-docx

---

## Repository Structure

```bash
applIQation/
├── backend/
│   ├── routers/
│   └── services/
│
├── frontend/
│   ├── src/
│   └── public/
│
├── src/
│   ├── data_generation/
│   ├── classical/
│   ├── deep_learning/
│   ├── evaluation/
│   └── deployment/
│
├── models/
│
├── data/
│
├── outputs/
│
└── README.md
```

---

## Installation

```bash
git clone https://github.com/eugeniatate/applIQation.git
cd applIQation
pip install -r requirements.txt
```

### Backend

```bash
cd backend
uvicorn backend.main:app --reload
```

Backend:
```
http://127.0.0.1:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

https://appliqation.vercel.app/ 

or locally:
```
http://localhost:5173
```

---- 
## API

Interactive API documentation is available at

https://appliqation-api-428926191821.us-central1.run.app/docs

Example endpoint

```text
POST /predict
```

Inputs

- Resume (PDF, DOCX, TXT)
- Job Description

Outputs

- Career readiness prediction
- Confidence score
- Skill match percentage
- Missing skills
- Personalized learning roadmap
  
--- 
## Future Work

- LLM-generated career coaching and interview preparation
- Capability graph construction for personalized learning paths
- Market-aware skill recommendations using real job postings
- Multi-role career planning and recommendation engine
- Integration with vector databases for semantic resume search
- Expanded evaluation using public resume-job datasets
- Enhanced visual analytics and explainability dashboards

---

## Author

**Eugenia Tate**

Duke University — Master of Engineering in Artificial Intelligence

