from src.config import PROFILE_DIR, RESUME_DIR

from src.data_generation.generate_candidate import (
    load_profile,
    generate_candidate
)

from src.data_generation.render_resume import (
    render_resume,
    save_resume
)

profile = load_profile(
    PROFILE_DIR / "ml_engineer.yaml"
)

candidate = generate_candidate(profile)

resume = render_resume(candidate)

print(resume)

save_resume(
    resume,
    candidate,
    RESUME_DIR
)