
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="example_python_package_billingsley",
    version="0.0.3",
    author="billingsley-john-testing",
    author_email="jhnbllngsly@gmail.com",
    description="Example python package",
    long_description=long_description,
    url="https://github.com/billingsley-john/example_python_package",
    packages=setuptools.find_packages()
)
