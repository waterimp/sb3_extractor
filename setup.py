from setuptools import setup, find_packages

with open("README.md", "r") as f:
    longdesc = f.read()

setup(
    name="sb3_extractor",
    version="0.0.1",
    description="Parse Scratch SB3 files and extract well-named asset files.",
    long_description=longdesc,
    long_description_content_type="text/markdown",
    url="https://github.com/waterimp/sb3_extractor",
    author="Lee Bush",
    license="GPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords="scratch sb3 converter extractor",
    packages=find_packages(),
    python_requires=">=3.6"
    )
