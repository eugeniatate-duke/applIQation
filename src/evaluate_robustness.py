import json
from pathlib import Path

from src.extract_skills import (
    load_taxonomy,
    extract_skills
)

from src.gap_analysis import analyze_gaps
from src.readiness import calculate_readiness

from src.llm_assessor import assess_candidate


taxonomy = load_taxonomy()


resume_path = "data/resumes/resume4.txt"

evaluation_files = [
    "docker_original.txt",
    "docker_variant_1.txt",
    "docker_variant_2.txt"
]


resume_text = Path(resume_path).read_text()

results = []

for filename in evaluation_files:

    jd_path = f"data/evaluation/{filename}"

    job_text = Path(jd_path).read_text()

    # Baseline
    resume_results = extract_skills(
        resume_text,
        taxonomy
    )

    job_results = extract_skills(
        job_text,
        taxonomy
    )

    gaps = analyze_gaps(
        resume_results,
        job_results
    )

    baseline_score = calculate_readiness(
        gaps,
        len(job_results["skills"])
    )

    # GPT
    llm_result = assess_candidate(
        resume_text,
        job_text,
        target_role="MLOps Engineer"
    )

    results.append({
        "scenario": filename,
        "baseline_score": baseline_score,
        "llm_score": llm_result["readiness_score"],
        "baseline_missing": gaps["missing"],
        "llm_gaps": llm_result["gaps"]
    })

with open(
    "outputs/evaluation_results.json",
    "w"
) as f:
    json.dump(
        results,
        f,
        indent=2
    )

print(json.dumps(results, indent=2))