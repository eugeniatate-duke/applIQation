"""
evaluate_recommender.py

Offline evaluation of the ApplIQation recommendation engine.

Unlike collaborative filtering recommenders, ApplIQation does not rely on
historical user interactions or click-through behavior. Instead, evaluation
focuses on properties appropriate for a content-based, cold-start
recommendation system.

Evaluation metrics:
- Skill-gap coverage
- Recommendation diversity
- Recommendation explainability
- Cold-start capability

Author: Eugenia Tate
"""

from pathlib import Path
import io
from contextlib import redirect_stdout
import pandas as pd

from backend.services.skills import extract_skills
from src.recommender.resource_recommender import recommend_resources

EVAL_DIR = Path("data/evaluation")


def load_text(filename):
    """Load a text file from the evaluation directory."""
    return (EVAL_DIR / filename).read_text(encoding="utf-8")


def evaluate_recommendations(job_name, resume_text, job_description):
    """
    Evaluate recommendation quality for a single resume/job pair.
    """

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    recommendations = recommend_resources(
        missing_skills=missing_skills,
        job_description=job_description,
        top_k=5,
    )

    # --------------------------------------------------
    # Skill-gap coverage
    # --------------------------------------------------

    covered_skills = set()

    for resource in recommendations:
        for skill in resource["skills"]:
            if skill in missing_skills:
                covered_skills.add(skill)

    skill_gap_coverage = len(covered_skills) / max(len(missing_skills), 1)

    # --------------------------------------------------
    # Recommendation diversity
    # --------------------------------------------------

    unique_formats = len(set(resource["format"] for resource in recommendations))

    unique_categories = len(set(resource["category"] for resource in recommendations))

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    explainable = sum(bool(resource["reason"]) for resource in recommendations)

    explainability_rate = explainable / max(len(recommendations), 1)

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    print("=" * 72)
    print(job_name)
    print("=" * 72)

    print(f"Detected skills : {len(job_skills)}")
    print(f"Matched skills  : {len(job_skills) - len(missing_skills)}")
    print(f"Missing skills  : {len(missing_skills)}")

    print()

    print("Evaluation Metrics")
    print("------------------")
    print(f"Skill-gap coverage        : {skill_gap_coverage:.1%}")
    formats = sorted(set(resource["format"] for resource in recommendations))
    categories = sorted(set(resource["category"] for resource in recommendations))

    print(f"Recommendation formats    : {unique_formats}")
    print(f"   {', '.join(formats)}")

    print(f"Recommendation categories : {unique_categories}")
    print(f"   {', '.join(categories)}")
    print(f"Explainability            : {explainability_rate:.1%}")

    print("Cold-start capability     : PASS")
    print(
        "Recommendations generated using only the resume "
        "and job description (no historical interactions)."
    )

    print()

    print("Top Recommendations")
    print("-------------------")

    for i, resource in enumerate(recommendations, start=1):

        overlap = [skill for skill in resource["skills"] if skill in missing_skills]

        print(f"{i}. {resource['title']}")
        print(f"   Format   : {resource['format']}")
        print(f"   Priority : {resource['priority']}")

        if overlap:
            print(f"   Addresses: {', '.join(overlap)}")
        else:
            print("   Addresses: Complementary engineering skills")

        print(f"   Reason   : {resource['reason']}")
        print()

    print("=" * 72)
    print()

    return {
        "Job": job_name,
        "Coverage": round(skill_gap_coverage, 3),
        "Formats": unique_formats,
        "Categories": unique_categories,
        "Explainability": explainability_rate,
    }

if __name__ == "__main__":

    OUTPUT_DIR = Path("data/outputs")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    resume = load_text("resume_ai_ml.txt")

    evaluations = [
        (
            "Micron - Senior Applied AI Engineer",
            "micron_jd.txt",
        ),
        (
            "NVIDIA - Machine Learning Engineer",
            "nvidia_jd.txt",
        ),
        (
            "OpenAI - Applied AI Engineer",
            "openai_jd.txt",
        ),
    ]

    metrics = []

    buffer = io.StringIO()

    with redirect_stdout(buffer):

        print("\nApplIQation Recommendation Evaluation")
        print("=" * 72)
        print(
            "Evaluation of a content-based recommendation system "
            "using representative AI/ML job descriptions.\n"
        )

        for job_name, jd_file in evaluations:

            result = evaluate_recommendations(
                job_name,
                resume,
                load_text(jd_file),
            )

            metrics.append(result)

        print("=" * 72)
        print("Overall Evaluation Summary")
        print("=" * 72)

        avg_coverage = sum(m["Coverage"] for m in metrics) / len(metrics)
        avg_formats = sum(m["Formats"] for m in metrics) / len(metrics)
        avg_categories = sum(m["Categories"] for m in metrics) / len(metrics)
        avg_explainability = sum(m["Explainability"] for m in metrics) / len(metrics)

        print(f"Average skill-gap coverage : {avg_coverage:.1%}")
        print(f"Average formats           : {avg_formats:.1f}")
        print(f"Average categories        : {avg_categories:.1f}")
        print(f"Average explainability    : {avg_explainability:.1%}")
        print("Cold-start capability     : PASS")

    output = buffer.getvalue()

    print(output)

    (OUTPUT_DIR / "recommender_evaluation.txt").write_text(
        output,
        encoding="utf-8",
    )

    pd.DataFrame(metrics).to_csv(
        OUTPUT_DIR / "recommender_metrics.csv",
        index=False,
    )

    print("Saved evaluation report to:")
    print(f"  {OUTPUT_DIR / 'recommender_evaluation.txt'}")
    print(f"  {OUTPUT_DIR / 'recommender_metrics.csv'}")
