from fastapi import APIRouter, UploadFile, File, Form
from services.skills import extract_skills

from services.parser import extract_resume_text
from src.deep_learning.inference import predict

router = APIRouter()

# ROADMAP = {
#     "Ready": [
#         "Continue applying to similar roles.",
#         "Practice technical and behavioral interviews.",
#         "Continue building your AI portfolio.",
#     ],
#     "Ready with Short Ramp-Up": [
#         "Learn Docker fundamentals.",
#         "Build one FastAPI project.",
#         "Deploy an ML application.",
#     ],
#     "Requires Significant Preparation": [
#         "Strengthen Python programming.",
#         "Complete an end-to-end ML project.",
#         "Learn Docker and FastAPI.",
#         "Practice SQL fundamentals.",
#     ],
# }


RECOMMENDED_SKILLS = {
    "Ready": [
        "LLMOps",
        "System Design",
        "Kubernetes",
    ],
    "Ready with Short Ramp-Up": [
        "Docker",
        "FastAPI",
        "AWS",
    ],
    "Requires Significant Preparation": [
        "Python",
        "Docker",
        "FastAPI",
        "SQL",
        "AWS",
    ],
}


@router.post("/predict")
async def predict_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    resume_text = extract_resume_text(resume)

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    matched_skills = [

        skill

        for skill in job_skills

        if skill in resume_skills

    ]

    missing_skills = [

        skill

        for skill in job_skills

        if skill not in resume_skills

    ]

    roadmap = []

    if "Docker" in missing_skills:
        roadmap.append("Learn Docker fundamentals.")

    if "AWS" in missing_skills:
        roadmap.append("Gain experience with AWS cloud services.")

    if "FastAPI" in missing_skills:
        roadmap.append("Build and deploy a FastAPI application.")

    if "SQL" in missing_skills:
        roadmap.append("Practice SQL through data engineering projects.")

    if "Machine Learning" in missing_skills:
        roadmap.append("Complete an end-to-end machine learning project.")

    if "Transformers" in missing_skills:
        roadmap.append("Fine-tune a transformer model on a custom dataset.")


    if not roadmap:

      roadmap.append(

          "Continue building production AI projects and applying for similar roles."

      )

    result = predict(
        resume_text,
        job_description,
    )

    label = result["label"]

    return {
        "label": label,
        "confidence": result["confidence"],
        # "recommended_skills": RECOMMENDED_SKILLS[label],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "roadmap": roadmap
    }
