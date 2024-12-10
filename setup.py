import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dream-api',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/DreamFaceAI/dream_api',
    license='MIT',
    author='DreamApi',
    description='DreamApi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    classifiers=[],
    python_requires='>=3.0'
)
