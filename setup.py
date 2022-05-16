from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyIntradel",
    version="0.0.2",
    description="Python interface for Intradel",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/thomasgermain/pyintradel.git",
    author="Thomas Germain",
    author_email="12560542+thomasgermain@users.noreply.github.com",
    license="MIT",
    packages=find_packages(exclude=("tests", "tests/*", "/tests", "/tests/*")),
    zip_safe=False,
    setup_requires=["pytest-runner"],
    install_requires=[
        "aiohttp>=3.8.0,<4.0.0",
        "beautifulsoup4>=4.11.0,<5.0.0",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
    ],
)
