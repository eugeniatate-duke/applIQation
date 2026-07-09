from src.config import JOB_PROFILE_DIR

from src.data_generation.generate_job import (
    load_job_profile,
    generate_job
)

profile = load_job_profile(
    JOB_PROFILE_DIR / "ml_engineer.yaml"
)

job = generate_job(profile)

print(job)