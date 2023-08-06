import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysql-framework",
    version="1.0.3",
    author="Rohit Chouhan",
    author_email="itsrohitofficial@gmail.com",
    description="Description regarding the package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohit-chouhan/pysql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
