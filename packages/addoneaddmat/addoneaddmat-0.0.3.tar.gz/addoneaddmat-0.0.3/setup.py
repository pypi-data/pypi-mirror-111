from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'Same as regular description'

setup(
    name="addoneaddmat",
    version=VERSION,
    author="Wayne Lam",
    author_email="",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['test', 'first package'],
    package_dir={"": "src"}
)