from setuptools import setup, find_packages, version


def readme():
    with open('README.md', encoding="utf8") as f:
        README = f.read()
    return README

setup(
    name="plagchecker",
    version="1.0.1",
    description="plagchecker focuses on using wwww.prepostseo.com plagairism checker facility.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    
    author="Shrey Patel",
    author_email="dailycodingpro@gmail.com",
    packages=['plagchecker'],
    install_requires=[],
    url="",
    keywords = ['plagairism', 'checker', 'plagairismchecker', 'prepostseo' ,'seo'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    include_package_data=False,
)