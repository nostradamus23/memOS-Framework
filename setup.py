"""
Setup configuration for MemOS AI Framework.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="memos-ai",
    version="0.1.0",
    author="MemOS AI Team",
    author_email="memosai@proton.me",
    description="A framework for transforming static memes into interactive digital entities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nostradamus23/memos-Framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "Pillow>=9.0.0",
        "opencv-python>=4.8.0",
        "scikit-learn>=1.0.0",
        "tensorflow>=2.13.0",
        "spacy>=3.6.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "python-multipart>=0.0.6",
        "pydantic>=2.0.0",
        "requests>=2.31.0",
        "aiohttp>=3.8.5",
        "sqlalchemy>=2.0.0",
        "alembic>=1.11.0",
        "redis>=4.6.0",
        "celery>=5.3.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "mypy>=1.4.0",
            "flake8>=6.1.0",
            "pre-commit>=3.3.3"
        ]
    },
    entry_points={
        "console_scripts": [
            "memos=memos.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 