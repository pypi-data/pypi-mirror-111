import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="galerkin-transformer",
    version="0.1.1",
    author="Shuhao Cao",
    author_email="scao.math@gmail.com",
    description="Fourier and Galerkin Transformer",
    long_description="Fourier and Galerkin Transformer: attention without softmax",
    long_description_content_type="text/markdown",
    url="https://github.com/scaomath/fourier-transformer",
    project_urls={
        "Bug Tracker": "https://github.com/scaomath/fourier-transformer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)