"""Setup script for AI-OS agent package."""

from setuptools import find_packages, setup

setup(
    name="ai-os-agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[],
)

