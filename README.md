# applIQation

## Project Scope

applIQation is designed specifically for **Artificial Intelligence, Machine Learning, Data Science, MLOps, and Software Engineering career paths**.

The system is **not intended to evaluate resumes for unrelated professional domains** such as healthcare, law, finance, accounting, marketing, or general human resources positions.

Restricting the application to technical AI and software engineering roles enables the model to learn domain-specific terminology, technical competencies, and resume-job relationships more effectively while avoiding unsupported predictions outside its intended scope.

### Recommendation Scope

The recommendation engine is designed to complement—not replace—the overall career readiness assessment.

A candidate may be classified as **Ready** while still receiving personalized learning recommendations. This reflects real-world hiring practices, where successful applicants rarely satisfy every listed qualification but may still benefit from strengthening specific technical competencies.

Similarly, recommendations may extend beyond explicitly missing keywords. For example, a resume that demonstrates general machine learning experience may still receive recommendations related to **fine-tuning**, **model evaluation**, or **ML system design** when those advanced competencies are important for the target role. The recommendation engine therefore prioritizes career development and long-term readiness rather than exact keyword completion.

Career readiness and personalized recommendations intentionally serve different purposes: the readiness assessment estimates current suitability for a target technical role, while the recommendation engine identifies opportunities for continued professional growth—even for candidates already considered ready to apply.

---

# Repository Organization

This repository contains multiple course projects built on the same application.

**Module 2 – NLP Project** :Transformer-based career readiness assessment using a fine-tuned DistilBERT model. ( `docs/README_NLP.md` )

 **Module 3 – Recommendation Systems** : Content-based learning recommender with explainable recommendations, cold-start support, and responsible recommendation design. (`docs/README_RECSYS.md` )

 **Module 4 – Generative AI** *(coming soon)* : Extension of the platform with LLM-powered career coaching and personalized learning guidance. (`docs/README_GENAI.md` )

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
