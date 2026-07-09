"""
setup.py

Installs the applIQation project as an editable Python package.

This allows project modules to be imported consistently
across tests, training scripts, notebooks, and the API.
"""

from setuptools import setup, find_packages

setup(
    name="appliqation",
    version="0.1.0",
    description="AI-powered career readiness assessment system",
    author="Eugenia Tate",
    packages=find_packages(),
    python_requires=">=3.10",
)