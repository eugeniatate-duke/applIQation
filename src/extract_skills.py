import json


def load_taxonomy(path="data/skills.json"):
    with open(path, "r") as f:
        return json.load(f)


def extract_skills(text, taxonomy):
    text = text.lower()

    found_skills = set()
    found_capabilities = set()

    for capability, skills in taxonomy.items():
        for skill in skills:
            if skill.lower() in text:
                found_skills.add(skill)
                found_capabilities.add(capability)

    return {
        "skills": sorted(list(found_skills)),
        "capabilities": sorted(list(found_capabilities))
    }