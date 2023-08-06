import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googlesearch.py",
    version="1.2",
    author="Sijey Praveen",
    author_email="cjpraveen@hotmail.com",
    description="Google Search Scrapper For Python Programming Language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sijey-Praveen/googlesearch.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = "googlesearch.py, python google search, google search pypi,sijey-praveen pypi, google api, sijey, sijey-praveen, sijey praveen projects",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
