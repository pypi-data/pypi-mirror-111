# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md')) as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="stocksent",
    version="0.1.5",
    description="A Python library for sentiment analysis of various tickers from the latest news from trusted sources and tools to plot results.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stocksent.readthedocs.io/",
    author="Arya Manjaramkar",
    author_email="aryagm01@email.com",
    license="Mozilla Public License 2.0 (MPL 2.0)",
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["stocksent"],
    include_package_data=True,
    install_requires=["numpy", "pandas",
                      "matplotlib", "nltk", "wordcloud", "bs4"]
)
