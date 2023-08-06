import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCondorRaven",
    version="1.0.0",
    author="Daniel Velasquez",
    author_email="daniel.velasquez@sura-am.com",
    description="Investment analytics and machine learning tools.",
    long_description="Investment analytics and machine learning tools.",
    long_description_content_type="text/markdown",
    url="https://github.com/valdanie/PyCondorRaven",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
