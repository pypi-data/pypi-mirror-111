import pathlib
from setuptools import setup
import setuptools



# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dataplotter",
    version="0.0.1",
    description="Generate plots from data",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Everyone",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages=['dataplotter'],
    install_requires=['matplotlib', 'plotly'],
    include_package_data=True,
)


# python setup.py sdist bdist_wheel

# twine upload dist/*