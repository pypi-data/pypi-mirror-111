import setuptools

with open(r"C:\Users\Phanindra Thorati\mypackage\README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stringsfuns",
    version="0.1",
    description="String functions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    author="Thorati Jai Satya Sai Phanindra",
    author_email="thoratiphanindra@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    zip_safe=False
)
