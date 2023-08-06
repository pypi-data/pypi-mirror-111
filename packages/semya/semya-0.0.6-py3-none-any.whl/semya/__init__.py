#!/usr/bin/env python
import importlib
import os
import sys
from codecs import open

from setuptools import find_packages, setup

from semya.__about__ import *  # noqa: F403,F401


class Semya:
    """Creates a setup file and class"""

    def __init__(
        self,
        package_name: str,
        *,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
        ],
        entry_points: dict = {},
        include_package_data: bool = False,
        long_description_content_type: str = "text/markdown",
        package_data: dict = {"": []},
        project_documentation_url: str = None,
        python_version: str = ">=3.7",
        zip_safe=False,
    ):
        """Initializes the setup object to create a package.

        Args:
            package_name (str): Name of the resulting package. If publishing to
                                pypi this needs to be globally unique.
            project_url (str): URL of the project
                               ex. https://github.com/user/package
            include_package_data (bool, optional): Include package
                                data with setup.Defaults to False.
            python_version (str, optional): Python version compatitbility.
                                            Defaults to ">=3.7".
            zip_safe (bool, optional): Safe to use package as a zip file.
                                       Defaults to False.
            classifiers (list): List of classifiers for setup.
        """
        self.package_name = package_name

        self.classifiers = classifiers
        self.entry_points = entry_points
        self.include_package_data = include_package_data
        self.long_description_content_type = long_description_content_type
        self.package_data = package_data
        self.python_version = python_version
        self.zip_safe = zip_safe

        repo_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.insert(0, repo_path)

        # Dynamic import based on name
        imported_module = importlib.import_module(package_name)
        self.about = getattr(imported_module, "__about__")

        # Set project source url from __about__ file
        self.project_source_url = self.about.__url__

        # Set project documentation url to the project url if it does not exist.
        if project_documentation_url is not None:
            self.project_documentation_url = project_documentation_url
        else:
            self.project_documentation_url = self.about.__url__

        self.packages = find_packages(
            where=repo_path,
            include=[package_name],
            exclude=[
                "examples",
            ],
        )

        # Open requirements files to grab package dependencies
        with open("requirements.txt") as f:
            self.install_requires = [line for line in f if "==" in line]

        with open("requirements-test.txt") as f:
            self.tests_require = [line for line in f if "==" in line]

        with open("requirements-dev.txt") as f:
            self.dev_requires = [line for line in f if "==" in line]

        with open("README.md", "r", "utf-8") as f:
            self.readme = f.read()

    def sew(self) -> None:
        """Sets up the package using the previously configured class."""
        setup(
            name=self.about.__title__,
            version=self.about.__version__,
            description=self.about.__description__,
            long_description=self.readme,
            long_description_content_type=self.long_description_content_type,
            author=self.about.__author__,
            author_email=self.about.__author_email__,
            url=self.about.__url__,
            packages=self.packages,
            package_dir={f"{self.package_name}": self.package_name},
            package_data=self.package_data,
            include_package_data=self.include_package_data,
            python_requires=self.python_version,
            install_requires=self.install_requires,
            setup_requires=self.install_requires,
            extras_require={
                "test": self.tests_require,
                "dev": self.dev_requires,
            },
            license=self.about.__license__,
            zip_safe=self.zip_safe,
            classifiers=self.classifiers,
            tests_require=self.tests_require,
            project_urls={
                "Source": self.project_source_url,
                "Documentation": self.project_documentation_url,
            },
        )
