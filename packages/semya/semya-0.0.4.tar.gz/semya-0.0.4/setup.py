#!/usr/bin/env python
import os
import sys
from codecs import open

from setuptools import find_packages, setup

# Import the package module code from local directory.
repo_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, repo_path)
from semya import __about__ as about  # noqa

packages = find_packages(
    where=repo_path,
    include=["gytrash"],
    exclude=[
        "examples",
    ],
)

# Open requirements files to grab package dependencies
with open("requirements.txt") as f:
    install_requires = [line for line in f if "==" in line]

with open("requirements-test.txt") as f:
    tests_require = [line for line in f if "==" in line]

with open("requirements-dev.txt") as f:
    dev_requires = [line for line in f if "==" in line]

# Open README file to attach readme as package description.
with open("README.md", "r", "utf-8") as f:
    readme = f.read()

# Setup package.
setup(
    name=about.__title__,
    version=about.__version__,
    description=about.__description__,
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about.__author__,
    author_email=about.__author_email__,
    url=about.__url__,
    packages=packages,
    package_dir={"gytrash": "gytrash"},
    package_data={"": []},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=install_requires,
    setup_requires=install_requires,
    extras_require={
        "test": tests_require,
        "dev": dev_requires,
    },
    license=about.__license__,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    tests_require=tests_require,
    project_urls={"Source": "https://github.com/trejas/gytrash"},
)
