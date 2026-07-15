from fastapi import APIRouter, UploadFile, File, Form
from src.recommender.resource_recommender import recommend_resources

from backend.services.parser import extract_resume_text
from backend.services.skills import extract_skills
from src.deep_learning.inference import predict

router = APIRouter()


@router.post("/predict")
async def predict_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    # --------------------------------------------------
    # Extract resume text
    # --------------------------------------------------

    resume_text = extract_resume_text(resume)

    # --------------------------------------------------
    # Skill matching
    # --------------------------------------------------

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = [skill for skill in job_skills if skill in resume_skills]

    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    if len(job_skills) == 0:
        skill_match = 1.0
    else:
        skill_match = len(matched_skills) / len(job_skills)

    # --------------------------------------------------
    # DistilBERT prediction
    # --------------------------------------------------

    result = predict(
        resume_text,
        job_description,
    )

    # --------------------------------------------------
    # Hybrid readiness decision
    # --------------------------------------------------

    if skill_match == 1.0:
        label = "Ready"

    elif skill_match >= 0.70:
        label = "Ready with Short Ramp-Up"

    else:
        label = result["label"]

    # --------------------------------------------------
    # Personalized learning roadmap
    # --------------------------------------------------

    roadmap = []

    if "Docker" in missing_skills:
        roadmap.append("Learn Docker fundamentals and containerize one project.")

    if "AWS" in missing_skills:
        roadmap.append("Gain hands-on AWS cloud experience.")

    if "FastAPI" in missing_skills:
        roadmap.append("Build and deploy a FastAPI application.")

    if "SQL" in missing_skills:
        roadmap.append("Practice SQL through realistic data engineering projects.")

    if "Machine Learning" in missing_skills:
        roadmap.append("Complete an end-to-end machine learning project.")

    if "Transformers" in missing_skills:
        roadmap.append("Fine-tune a transformer model on a custom dataset.")

    if not roadmap:
        roadmap = [
            "Your resume demonstrates strong technical alignment with the job description.",
            "Continue preparing for technical interviews.",
            "Keep building production-quality AI projects.",
        ]
    # -------------------------------------------
    # Recommended Resources
    # -------------------------------------------
    recommended_resources = recommend_resources(
        missing_skills=missing_skills,
        job_description=job_description,
        top_k=5,
    )

    # --------------------------------------------------
    # Response
    # --------------------------------------------------

    return {
        "label": label,
        "confidence": result["confidence"],
        "skill_match": round(skill_match * 100, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_count": len(matched_skills),
        "required_count": len(job_skills),
        "roadmap": roadmap,
        "recommended_resources": recommended_resources,
    }
