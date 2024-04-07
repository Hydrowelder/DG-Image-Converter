from setuptools import setup, find_packages

setup(
    name="imageconverter",
    version="1.0",
    packages=['imageconverter'],
    package_dir={'':'src'},
    install_requires=["numpy", "pathlib", "pillow"],
)