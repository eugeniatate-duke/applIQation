# ApplIQation – Personalized Career Path Recommender

Vercel App: https://appliqation.vercel.app/

Backend API (Google Cloud Run): https://appliqation-api-428926191821.us-central1.run.app/docs

### Recommendation Systems Extension

ApplIQation extends the NLP career readiness assessment into a **content-based recommendation system** that generates personalized learning recommendations based on detected technical skill gaps between a candidate's resume and a target AI/ML job description.

Rather than optimizing for clicks or engagement, the system recommends educational resources that maximize **career readiness**, helping candidates focus on the highest-impact skills needed for technical AI and software engineering roles.


Developed for **AIPI 540 – Deep Learning Applications** at Duke University.

---

# Project Scope

ApplIQation is designed specifically for:

- Artificial Intelligence
- Machine Learning
- Data Science
- MLOps
- Software Engineering

The recommendation engine is **not intended** for general career counseling or non-technical professions such as healthcare, law, accounting, finance, marketing, or human resources.

Restricting the recommendation space allows recommendations to remain domain-specific, explainable, and actionable.

### Recommendation Scope

The recommendation engine is designed to complement—not replace—the overall career readiness assessment.

A candidate may be classified as **Ready** while still receiving personalized learning recommendations. This reflects real-world hiring practices, where successful applicants rarely satisfy every listed qualification but may still benefit from strengthening specific technical competencies.

Similarly, recommendations may extend beyond explicitly missing keywords. For example, a resume that demonstrates general machine learning experience may still receive recommendations related to **fine-tuning**, **model evaluation**, or **ML system design** when those advanced competencies are important for the target role. The recommendation engine therefore prioritizes career development and long-term readiness rather than exact keyword completion.

Career readiness and personalized recommendations intentionally serve different purposes: the readiness assessment estimates current suitability for a target technical role, while the recommendation engine identifies opportunities for continued professional growth—even for candidates already considered ready to apply.

---

# Recommendation Problem

After the NLP model predicts overall career readiness, users still face an important question:

> **What should I learn next?**

Traditional learning platforms typically recommend popular courses or resources without considering a candidate's existing technical background or the requirements of a specific target job.

ApplIQation instead recommends learning resources that directly address the candidate's identified technical skill gaps.

---

# Recommendation Solution

ApplIQation uses a **content-based recommendation system**.

Unlike collaborative filtering recommenders, the system does **not** require:

- historical user interactions
- click-through history
- ratings
- purchase history

Instead, recommendations are generated using only:

- Candidate resume
- Target job description
- Technical skill gap analysis

This allows recommendations to be generated immediately for first-time users (cold-start scenario).

---

# Recommendation Pipeline

```text
Resume
      │
      ▼
Skill Extraction
      │
      ▼
Canonical Skill Dictionary
      │
      ▼
Gap Analysis
      │
      ▼
TF-IDF + Cosine Similarity
      │
      ▼
Skill Coverage Weighting
      │
      ▼
Diversity-aware Ranking
      │
      ▼
Personalized Learning Recommendations
```

---

# Recommendation Features

The recommendation engine incorporates several practical design considerations.

### Cold Start

Recommendations require no historical user interactions.

Only the uploaded resume and target job description are needed.

### Explainability

Every recommendation includes a human-readable explanation describing why the resource was selected.

### Diversity

Recommendations intentionally include multiple resource types, including:

- Courses
- Documentation
- Projects
- Books
- Interactive tutorials

This avoids recommending only one learning format.

### Skill Coverage

Recommendations prioritize resources that address detected technical skill gaps while still considering semantic similarity and resource popularity.

---

# Recommendation Algorithm

The final recommendation score combines multiple signals:

- TF-IDF cosine similarity between the user's missing skills and learning resources
- Explicit skill-gap coverage
- Resource popularity
- Diversity-aware reranking

This balances semantic relevance with practical usefulness.

---

# Evaluation

Because ApplIQation is a **content-based cold-start recommendation system**, traditional collaborative filtering metrics such as:

- Precision@K
- Recall@K
- MAP
- NDCG

are not appropriate because no historical user-item interaction dataset exists.

Instead, evaluation focuses on measurable properties directly aligned with the system's design goals.

## Evaluation Metrics

- Skill-gap coverage
- Recommendation diversity
- Recommendation explainability
- Cold-start capability

Evaluation was performed using a sample tech resume and three representative AI engineering job descriptions:

- Micron – Senior Applied AI Engineer
- NVIDIA – Machine Learning Engineer
- OpenAI – Applied AI Engineer

### Evaluation Results

| Job | Skill-Gap Coverage | Formats | Categories | Explainability |
|------|------------------:|---------:|-----------:|---------------:|
| Micron | 42.9% | 3 | 4 | 100% |
| NVIDIA | 100.0% | 2 | 2 | 100% |
| OpenAI | 66.7% | 2 | 4 | 100% |
| **Average** | **69.8%** | **2.3** | **3.3** | **100%** |

Evaluation artifacts are automatically generated by:

```bash
python -m src.evaluation.evaluate_recommender
```

Outputs:

```text
data/outputs/recommender_evaluation.txt
data/outputs/recommender_metrics.csv
```

---

# Responsible Recommendation Design

Unlike commercial recommendation systems that optimize for engagement, ApplIQation prioritizes educational usefulness.

Recommendations are generated according to:

- Technical skill gaps
- Career readiness
- Recommendation diversity
- Transparent explanations

rather than popularity or user engagement.

---

# Deployment

```text
React (Vercel)
        │
        ▼
FastAPI (Google Cloud Run)
        │
        ▼
DistilBERT + Recommendation Engine
```

---

# Technologies Used

### Frontend

- React
- Axios
- Vercel

### Backend

- FastAPI
- Google Cloud Run

### Recommendation Engine

- TF-IDF
- Cosine Similarity
- Scikit-learn
- Content-based Filtering

### NLP

- DistilBERT
- Hugging Face Transformers
- PyTorch

---

# Future Work

The recommendation engine serves as the second stage of a larger AI career development platform.

Planned future work includes:

- LLM-generated AI Career Mentor
- Personalized interview preparation
- Adaptive learning plans
- Live labor-market trend integration
- Vector database retrieval of learning resources
- User feedback loops for continual recommendation refinement

---

# Author

**Eugenia Tate**

Duke University — Master of Engineering in Artificial Intelligence
