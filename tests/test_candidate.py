# test_candidate.py
from src.config import PROFILE_DIR

from src.data_generation.generate_candidate import (
    load_profile,
    generate_candidate
)

profile = load_profile(
    PROFILE_DIR / "ml_engineer.yaml"
)

candidate = generate_candidate(profile)

print(candidate)