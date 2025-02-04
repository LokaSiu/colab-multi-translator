from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="colab-multi-translator",
    version="0.1.0",
    author="Loka Siu",
    description="An educational multi-translator interface for Google Colab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LokaSiu/colab-multi-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "ipython>=7.0.0",
    ],
)
