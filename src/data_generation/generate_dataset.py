"""
generate_dataset.py

Generates a synthetic career readiness dataset.

For each career archetype:
    1. Generate a synthetic candidate.
    2. Render a resume.
    3. Select a random target job.
    4. Calculate the readiness label.
    5. Save candidate and resume.
    6. Add an example to the training dataset.

The final dataset is saved as a CSV and will later be used
to train the baseline, classical ML, and deep learning models.
"""

import random
from src.data_generation.job_selection import (
    CAREER_MAP,
    JOB_FILES,
)

from src.data_generation.render_job import (
    render_job,
)
from src.config import JOB_DESCRIPTION_DIR

from src.data_generation.save_dataset import (
    save_candidate,
    save_dataset,
    save_job_description,
)

from src.config import (
    PROFILE_DIR,
    JOB_PROFILE_DIR,
    RESUME_DIR,
    CANDIDATE_DIR,
    PROCESSED_DIR,
)

from src.data_generation.generate_candidate import (
    load_profile,
    generate_candidate,
)

from src.data_generation.generate_job import (
    load_job_profile,
    generate_job,
)

from src.data_generation.render_resume import (
    render_resume,
    save_resume,
)

from src.data_generation.labeling import (
    calculate_readiness,
)


def load_yaml_files(directory):
    """
    Return all YAML files inside a directory.
    """
    return sorted(directory.glob("*.yaml"))


# def build_job_text(job):
#     """
#     Convert a structured job object into plain text.
#     This text becomes the model input for training.
#     """
#     lines = []

#     lines.append(job["title"])
#     lines.append("")
#     lines.append("Required Skills:")

#     for skill in job["required_skills"]:
#         lines.append(f"- {skill}")

#     lines.append("")
#     lines.append(f"Required Experience: {job['required_experience']} years")

#     lines.append(f"Preferred Education: {job['preferred_education']}")

#     return "\n".join(lines)


def generate_dataset(
    samples_per_profile=100,
    random_seed=42,
):
    """
    Generate a complete synthetic training dataset.

    Parameters
    ----------
    samples_per_profile : int

    random_seed : int
    """

    random.seed(random_seed)
    dataset = []
    candidate_profiles = load_yaml_files(PROFILE_DIR)
    # job_profiles = load_yaml_files(JOB_PROFILE_DIR)
    example_id = 1

    for profile_path in candidate_profiles:
        profile = load_profile(profile_path)
        for _ in range(samples_per_profile):

            # -------------------------
            # Generate candidate
            # -------------------------

            candidate = generate_candidate(profile)
            resume_text = render_resume(candidate)

            save_resume(resume_text,candidate,RESUME_DIR,)
            save_candidate(candidate,CANDIDATE_DIR,)

            # -------------------------------------------------------
            # Generate MULTIPLE job pairings for each candidate
            # -------------------------------------------------------

            career = CAREER_MAP[candidate["role"]]

            job_titles = career["primary_jobs"] + career["secondary_jobs"] + career["stretch_jobs"]

            for selected_title in job_titles:

                selected_job = JOB_PROFILE_DIR / JOB_FILES[selected_title]

                job_profile = load_job_profile(selected_job)

                job = generate_job(job_profile)

                job_text = render_job(job)

                result = calculate_readiness(
                    candidate,
                    job,
                )

                dataset.append(
                    {
                        "example_id": example_id,
                        "candidate_id": candidate["id"],
                        "role": candidate["role"],
                        "job_title": job["title"],
                        "resume_text": resume_text,
                        "job_text": job_text,
                        "readiness_score": result["score"],
                        "readiness_label": result["label"],
                    }
                )

                example_id += 1

    output_file = (PROCESSED_DIR /"career_readiness_dataset.csv")

    save_dataset(dataset,output_file,)

    print(f"\nGenerated {len(dataset)} examples.")
    print(f"Dataset saved to:\n{output_file}")


if __name__ == "__main__":
    generate_dataset(samples_per_profile=100)
