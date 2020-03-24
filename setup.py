import setuptools
import fsdict

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fsdict",
    version=str(fsdict.__version__),
    author="FranchuFranchu",
    author_email="fff999abc999@gmail.com",
    description="Store python dictionaries in a mixed directory/file structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FranchuFranchu/fsdict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
