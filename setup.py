import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typedtsv",
    version="0.6.0",
    author="jimmybot",
    author_email="jimmybot@jimmybot.com",
    description="A simple format for typed TSVs with an implementation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jimmybot/typedtsv",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)

