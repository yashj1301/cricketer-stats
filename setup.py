from setuptools import setup, find_packages

#encoding utf-8 for long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# reading requirements from requirements.txt
req = open("requirements.txt").readlines()
req = [x.strip("\n") for x in req]

# creating setup function to create the package
setup(
    name="scripts",
    version="0.4.0",
    author="Yash Jain",
    author_email="yash.jain106@gmail.com",
    description="A package for scraping, loading, and aggregating cricket player statistics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"":"scripts"},
    packages=find_packages(where="scripts", exclude=["tests","tests.*"]),
    include_package_data=True,
    install_requires=req
)

