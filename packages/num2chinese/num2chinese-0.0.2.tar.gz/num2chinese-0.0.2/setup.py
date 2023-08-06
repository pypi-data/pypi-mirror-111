import setuptools # type: ignore 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="num2chinese",
    version="0.0.2",
    author="kota",
    author_email="nicolaskodak@gmail.com",
    description="A nlp tool to transform numbers to Chinese characters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linpershey/num2chinese",
    project_urls={
        "Bug Tracker": "https://github.com/linpershey/num2chinese/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "./"},
    packages=setuptools.find_packages(where="./"),
    python_requires=">=3.6",
)
