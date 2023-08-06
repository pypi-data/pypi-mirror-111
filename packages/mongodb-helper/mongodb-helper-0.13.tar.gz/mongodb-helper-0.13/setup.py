import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mongodb-helper",
    version="0.13",
    author="Flampt",
    description="Methods that simplify MongoDB collection reading and writing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FlamptX/mongodb-helper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pymongo',
    ],
    keywords='mongodb, helper, mongodbhelper',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
