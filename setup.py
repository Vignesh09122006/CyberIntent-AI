"""Setup configuration for CyberIntent-AI package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cybersecurity-intent-ai",
    version="0.1.0",
    author="Vignesh",
    author_email="vignesh@example.com",
    description="AI-powered cybersecurity threat detection and intent prediction system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vignesh09122006/CyberIntent-AI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.940",
        ],
    },
    entry_points={
        "console_scripts": [
            "cybersecurity-intent=api.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
