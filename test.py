from pathlib import Path

from src.extract_skills import (
    load_taxonomy,
    extract_skills
)

from src.gap_analysis import analyze_gaps
from src.readiness import calculate_readiness


taxonomy = load_taxonomy()


resume_path = "data/resumes/resume1.txt"
job_path = "data/job_descriptions/ml-eng.txt"


resume_text = Path(resume_path).read_text()
job_text = Path(job_path).read_text()


resume_results = extract_skills(
    resume_text,
    taxonomy
)

job_results = extract_skills(
    job_text,
    taxonomy
)

gap_results = analyze_gaps(
    resume_results,
    job_results
)

readiness = calculate_readiness(
    gap_results,
    len(job_results["skills"])
)

print("\n===== APPLIQATION =====\n")

print("Readiness Score:")
print(f"{readiness}%\n")

print("Matched Skills:")
print(gap_results["matched"])

print("\nMissing Skills:")
print(gap_results["missing"])

print("\nResume Capabilities:")
print(resume_results["capabilities"])

print("\nJob Capabilities:")
print(job_results["capabilities"])