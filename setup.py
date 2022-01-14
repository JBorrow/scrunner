import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("scrunner/version.py", "r") as fh:
    exec(fh.read())

setuptools.setup(
    name="scrunner",
    version=__version__,
    author="Josh Borrow",
    author_email="josh@joshborrow.com",
    description="Runs scripts with associated metadata and puts together a summary page.",
    url="https://github.com/jborrow/scrunner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    scripts=["scrun"],
    install_requires=["attrs>=21.0.0", "jinja2>3.0.0"],
)
