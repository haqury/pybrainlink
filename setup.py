"""Setup configuration for PyBrainLink package"""

from setuptools import setup, find_packages
import pathlib

# Read README for long description
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="pybrainlink",
    version="0.2.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python library for BrainLink EEG devices",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/pybrainlink",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "bleak>=0.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.20",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    keywords="brainlink eeg bluetooth ble neuroscience brain",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/pybrainlink/issues",
        "Source": "https://github.com/YOUR_USERNAME/pybrainlink",
    },
)
