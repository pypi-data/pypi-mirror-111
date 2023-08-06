import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solvesudoku",
    version="0.0.2",
    author="Raj Srikar",
    author_email="rajsrikar.d161@gmail.com",
    description="Solves Sudoku within seconds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raj-Srikar/solvesudoku",
    project_urls={
        "Documentation": "https://github.com/Raj-Srikar/solvesudoku/wiki#documentation",
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
