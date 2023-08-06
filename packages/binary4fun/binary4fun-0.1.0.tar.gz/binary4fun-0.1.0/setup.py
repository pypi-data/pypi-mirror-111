import pathlib

from setuptools import find_packages, setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()


def get_version(rel_path: str):
    file_path = pathlib.Path(__file__).parent.absolute() / rel_path
    for line in file_path.read_text().splitlines():
        if line.startswith("__version__"):
            return line.split('"')[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="binary4fun",
    version=get_version("src/binary4fun/__init__.py"),
    author="Moritz Körber",
    author_email="moritz.koerber@gmail.com",
    description="binary4fun is a small game, which tries to guess a number between 1 and 100 by binary search.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/moritzkoerber/binary4fun",
    keywords="game, binary search",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3",
)
