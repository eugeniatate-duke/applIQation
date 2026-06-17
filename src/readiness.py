def calculate_readiness(gap_results, total_job_skills):

    if total_job_skills == 0:
        return 0

    matched_count = len(gap_results["matched"])

    score = round(
        (matched_count / total_job_skills) * 100,
        1
    )

    return score