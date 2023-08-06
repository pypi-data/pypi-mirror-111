from setuptools import setup, find_packages

__version__ = "1.0.0"

with open("README.md") as f:
    long_description = f.read()

setup(
    name="no-recursion",
    version=__version__,
    author="Jonathan",
    author_email="pybots.il@gmail.com",
    description="This module helps you to get rid of recursions when you want"
                "to rename a builtin function, or a function that already exists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonatan1609/noRecursion",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5"
)
