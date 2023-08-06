import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="concealment",
    version="0.0.3",
    description="privacy preservation for machine learning",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/concealment",
    author="microprediction",
    author_email="vaik@mit.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["concealment"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["wheel","pathlib"]
)
