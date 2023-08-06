import setuptools # type: ignore 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="num2chinese",
    version="0.0.1",
    author="kota",
    author_email="nicolaskodak@gmail.com",
    description="A nlp tool to transform numbers to Chinese characters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/num2chinese/0.0.0/",
    project_urls={
        "Bug Tracker": "https://github.com/linpershey/num2chinese/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "num2chinese"},
    packages=setuptools.find_packages(where="num2chinese"),
    python_requires=">=3.6",
)
