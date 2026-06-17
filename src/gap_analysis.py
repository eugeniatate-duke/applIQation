def analyze_gaps(resume_results, job_results):

    resume_skills = set(resume_results["skills"])
    job_skills = set(job_results["skills"])

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    return {
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing))
    }