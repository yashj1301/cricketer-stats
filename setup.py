from setuptools import setup, find_packages

setup(
    name="scripts",
    version="0.3",
    package_dir={"":"scripts"},
    packages=find_packages(where="scripts", exclude=["tests","tests.*"]),
    include_package_data=True
)