from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zycelium.dataconfig",
    version="0.0.3",
    description="Create dataclasses backed by configuration files.",
    author="Harshad Sharma",
    author_email="harshad@sharma.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zycelium/dataconfig",
    project_urls={
        "Bug Tracker": "https://github.com/zycelium/dataconfig/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=['zycelium.dataconfig'],
    package_dir={"": "src"},
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0",
        "configobj>=5.0",
    ],
    extras_require={
        "devel": [
            "bump2version>=1.0",
            "pytest>=6.2",
        ],
    },
)
