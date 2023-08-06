import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csvtea-elunico",
    version="3.0.1",
    author="Thomas Povinelli",
    author_email="author@example.com",
    description="A flexible, extensible, pluggable, slightly-out-of-spec CSV parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/elunico/CSVTea",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
