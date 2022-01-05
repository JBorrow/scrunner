import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrunner",
    version="0.0.0",
    author="Josh Borrow",
    author_email="borrowj@mit.edu",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=["attr"],
)
