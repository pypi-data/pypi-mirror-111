"""The setup script."""
from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author_email="paul@caston.id.au",
    author="Paul Caston",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Get the latest Open Peer Power version from various sources.",
    install_requires=[
        "aiohttp>=3.6.1,<4.0",
        "async_timeout<=3.0.1",
        "awesomeversion>=21.2.3",
    ],
    keywords=["openpeerpower", "version", "update"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="pyopversion",
    packages=find_packages(include=["pyopversion"]),
    python_requires=">=3.8.0",
    url="https://github.com/pcaston/pyopversion",
    version="3.5.0",
)
