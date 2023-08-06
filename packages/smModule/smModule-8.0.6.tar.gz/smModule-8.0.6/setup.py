import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smModule",
    version="8.0.6",
    author="Pascal Vallaster",
    description="SM: contains a wide range of useful pythons things, for instance: " +
                "SQL/XML/JSON - engine,math-functions, Log-writer, Terminal-Animations and CopyPast-Section.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["sm"],
    package_dir={'': 'sm/src'},
    install_requires=[]
)
