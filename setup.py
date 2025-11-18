"""
Setup script for Nature-Based Financial Risk Analysis package
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = [
        'pandas>=1.3.0',
        'numpy>=1.20.0',
        'scipy>=1.7.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'joblib>=1.0.0',
        'openpyxl>=3.0.0',
    ]

setup(
    name="nature-analysis",
    version="2.0.0",
    author="Nature Analysis Team",
    author_email="",
    description="Quantify how ecosystem service disruptions impact financial portfolios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shs-nature-analysis",
    packages=find_packages(include=['nature_analysis', 'nature_analysis.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.9',
            'mypy>=0.900',
        ],
    },
    entry_points={
        'console_scripts': [
            'nature-analysis=nature_analysis.pipeline:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
