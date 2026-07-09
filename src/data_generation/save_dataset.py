"""
save_dataset.py

Helper functions for saving generated synthetic data.

This module is responsible for writing candidate objects,
rendered resumes, and the final dataset to disk.
"""

import json
from pathlib import Path
import pandas as pd


def save_candidate(candidate, output_directory):
    """
    Save a candidate object as JSON.

    Parameters
    ----------
    candidate : dict
        Candidate object generated from a career archetype.

    output_directory : Path
        Directory where JSON files should be written.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    role = (candidate["role"]
        .lower()
        .replace(" ", "_")
    )

    filename = (
        output_directory /
        f"{role}_{candidate['id']}.json"
    )

    with open(filename, "w") as f:
        json.dump(candidate, f, indent=4)


def save_dataset(dataset, output_file):
    """
    Save the generated dataset as a CSV.

    Parameters
    ----------
    dataset : list[dict]
    output_file : Path
    """

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.DataFrame(dataset)

    df.to_csv(
        output_file,
        index=False
    )

def save_job_description(job_text, job, output_directory):
    """
    Save a rendered job description.

    Parameters
    ----------
    job_text : str
    job : dict
    output_directory : Path
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    title = job["title"].lower().replace(" ", "_")
    filename = output_directory / f"{title}.txt"

    with open(filename, "w") as f:
        f.write(job_text)