# type: ignore
from setuptools import find_packages, setup

requirements = [
    "scipy",
    "xarray",
    "pandas",
]

source_requirements = []

setup(
    name="pySESL",
    use_scm_version=True,
    author="Ian Bolliger",
    description="Semi-empirical Sea Level Estimator",
    author_email="ibolliger@rhg.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    dependency_links=source_requirements,
)
