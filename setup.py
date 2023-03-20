import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FileMapper",
    version="1.0.0",
    author="AndrewWritesCode",
    description="Stores map of directory structure in Python dictionary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndrewWritesCode/File-Mapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
