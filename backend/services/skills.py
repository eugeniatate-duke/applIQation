KNOWN_SKILLS = [
    "Python",
    "Docker",
    "FastAPI",
    "SQL",
    "AWS",
    "PyTorch",
    "TensorFlow",
    "Transformers",
    "Machine Learning",
    "Deep Learning",
    "Git",
    "Linux",
    "Kubernetes",
    "MLflow",
    "Pandas",
    "NumPy",
]


def extract_skills(text):
    """
    Extract known skills from text.
    """

    text = text.lower()

    found = []

    for skill in KNOWN_SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return sorted(found)
