import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecalculator-pkg-linda-oranya",
    version="0.0.2",
    author="Linda Oranya",
    author_email="oranyalinda7@gmail.com",
    description="A calculator written in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linda-oranya/pypi_calculator",
    project_urls={
        "Bug Tracker": "https://github.com/linda-oranya/pypi_calculator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)