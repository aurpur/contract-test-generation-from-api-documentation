from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="contract-test-generation",
    version="0.1.0",
    author="Aurel IKAMA HONEY",
    description="Multi-Agent System for Contract Test Generation from API Documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aurpur/contract-test-generation-from-api-documentation",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "isort>=5.13.2",
            "mypy>=1.7.1",
            "pylint>=3.0.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "contract-test-gen=src.main:main",
        ],
    },
)
