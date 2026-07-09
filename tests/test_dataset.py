import json
from pathlib import Path
from src.llm_assessor import assess_candidate
import pandas as pd

from src.extract_skills import (
    load_taxonomy,
    extract_skills
)

from src.gap_analysis import analyze_gaps
from src.readiness import calculate_readiness


# taxonomy = load_taxonomy()


# resume_path = "data/resumes/resume1.txt"
# job_path = "data/job_descriptions/ml-eng.txt"


# resume_text = Path(resume_path).read_text()
# job_text = Path(job_path).read_text()

# llm_result = assess_candidate(
#     resume_text,
#     job_text,
#     target_role="ML Engineer"
# )

# resume_results = extract_skills(
#     resume_text,
#     taxonomy
# )

# job_results = extract_skills(
#     job_text,
#     taxonomy
# )

# gap_results = analyze_gaps(
#     resume_results,
#     job_results
# )

# readiness = calculate_readiness(
#     gap_results,
#     len(job_results["skills"])
# )

# print("\n===== APPLIQATION =====\n")

# print("Readiness Score:")
# print(f"{readiness}%\n")

# print("Matched Skills:")
# print(gap_results["matched"])

# print("\nMissing Skills:")
# print(gap_results["missing"])

# print("\nResume Capabilities:")
# print(resume_results["capabilities"])

# print("\nJob Capabilities:")
# print(job_results["capabilities"])

# print("\n===== LLM ASSESSMENT =====\n")

# print(
#     f"Readiness Score: "
#     f"{llm_result['readiness_score']}"
# )

# print(
#     f"Recommendation: "
#     f"{llm_result['recommendation']}"
# )

# print("\nStrengths:")
# for item in llm_result["strengths"]:
#     print("-", item)

# print("\nGaps:")
# for item in llm_result["gaps"]:
#     print("-", item)

# print("\nAssessment Questions:")
# for i, q in enumerate(
#     llm_result["assessment_questions"],
#     start=1
# ):
#     print(f"{i}. {q}")


# with open("outputs/sample_output.json", "w") as f:
#     json.dump(llm_result, f, indent=2)

df = pd.read_csv("data/processed/career_readiness_dataset.csv")

print(df.head())

print("\nLabel Distribution:\n")

print(df["readiness_label"].value_counts())