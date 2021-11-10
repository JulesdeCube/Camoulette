import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="camoulette",
    version="1.0.0",
    author="Jules Lefebvre",
    author_email="jules.lefebvre@epita.fr",
    description="A python class base test suite package to automate ocaml "
                "practice and final grading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JulesdeCube/Camoulette",
    project_urls={
        "Bug Tracker": "https://github.com/JulesdeCube/Camoulette/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.8",
)
