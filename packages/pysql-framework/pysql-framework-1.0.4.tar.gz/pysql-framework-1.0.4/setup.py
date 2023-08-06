import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysql-framework",
    version="1.0.4",
    author="Rohit Chouhan",
    author_email="itsrohitofficial@gmail.com",
    description="PySQL is database framework for Python (v3.x) Language, Which is based on Python module mysql.connector, this module can help you to make your code more short and more easier. Before using this framework you must have knowledge about list, tuple, set, dictionary because all codes are designed using it. It's totally free and open source.",
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
