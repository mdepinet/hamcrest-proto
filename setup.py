import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hamcrest_proto",
    version="0.0.6",
    author="mdepinet",
    author_email="",
    description="Hamcrest matchers for protobufs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdepinet/hamcrest-proto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
