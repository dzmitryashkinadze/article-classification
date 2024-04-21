from setuptools import setup

setup(
    name="recommender",
    version="0.1.0",
    description="A package to reccomend MDPI journals based on the user input",
    author="Dzmitry Ashkinadze",
    author_email="dzmitry.ashkinadze@accenture.com",
    packages=["recommender"],
    install_requires=[
        "openai",
    ],
)
