from setuptools import setup, find_packages
from PyroPara import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="PyroPara",
    version=__version__,
    author="Majer",
    author_email="Majer.Krystof@gmail.com",
    description="Analysis toll for obtaining Arrhenius equation parameters from pyrolisis data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Krystof-Majer/PyroPara.git",
    license="MIT",
    install_requires=["numpy", "PySide6", "matplotlib", "scipy"],
    extras_require={
        "dev": [
            "pytest",
            "pytest-html",
            "autopep8",
            "autoflake",
            "black",
            "isort",
            "mypy",
            "tox",
            "flake8",
            "coverage",
            "matplotlib",
            "scipy",
        ]
    },
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    entry_points={
        "gui_scripts": [
            "PyroPara=PyroPara.gui:show",
        ]
    },
)
