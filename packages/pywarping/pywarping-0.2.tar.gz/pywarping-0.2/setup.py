from setuptools import setup
import os

import pywarping

with open("README.md", "r") as fh:
    long_description = fh.read()
    
INSTALL_REQUIRES = [
    "click>=7.0",
    "matplotlib>=2.0.0",
    "numpy>=1.16.4",
    "opencv-python",
    "scikit-image",
]

if "RTD_BUILD" not in os.environ:
    # ReadTheDocs cannot handle compilation
    INSTALL_REQUIRES += ["dlib"]

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/dopevog/pywarping/issues",
    "Documentation": "https://pywarping.readthedocs.io",
    "Source Code": "https://github.com/dopevog/pywarping",
}
VERSION = pywarping.__version__

setup(
    name="pywarping",
    version=VERSION,
    author="Vedant Kothari",
    author_email="dopevog@gmail.com",
    description="Automated face warping tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dopevog/pywarping",
    project_urls=PROJECT_URLS,
    packages=["pywarping"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        ("Programming Language :: Python :: " "Implementation :: CPython"),
    ],
    python_requires='>=3.5',
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": ["codecov", "flake8", "pydocstyle", "pytest>=3.6", "pytest-cov", "tox"],
        "docs": ["sphinx", "sphinx_rtd_theme"],
    },
    entry_points={"console_scripts": ["pw = pywarping.cli:cli"]},
)
