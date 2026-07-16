# applIQation

## Project Scope

applIQation is designed specifically for **Artificial Intelligence, Machine Learning, Data Science, MLOps, and Software Engineering career paths**.

The system is **not intended to evaluate resumes for unrelated professional domains** such as healthcare, law, finance, accounting, marketing, or general human resources positions.

Restricting the application to technical AI and software engineering roles enables the model to learn domain-specific terminology, technical competencies, and resume-job relationships more effectively while avoiding unsupported predictions outside its intended scope.

---

# Repository Organization

This repository contains multiple course projects built on the same application.

| Component | Description | Documentation |

|-----------|-------------|---------------|

| **Module 2 – NLP Project** | Transformer-based career readiness assessment using a fine-tuned DistilBERT model. | `docs/README_NLP.md` |

| **Module 3 – Recommendation Systems** | Content-based learning recommender with explainable recommendations, cold-start support, and responsible recommendation design. | `docs/README_RECSYS.md` |

| **Module 4 – Generative AI** *(in progress)* | Extension of the platform with LLM-powered career coaching and personalized learning guidance. | `docs/README_GENAI.md` |

---

# Deployment

**Frontend (React + Vercel)**

https://appliqation.vercel.app/

**Backend (FastAPI + Google Cloud Run)**

https://appliqation-api-428926191821.us-central1.run.app/docs

---

# Technologies

- React
- FastAPI
- DistilBERT
- PyTorch
- Hugging Face Transformers
- Scikit-learn
- Google Cloud Run
- Vercel

---

## Frontend Dependencies

Frontend dependencies are managed separately through:

```text
frontend/package.json
```

Python dependencies are listed in:

```text
requirements.txt
```
