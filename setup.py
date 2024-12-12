import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dream-api',
    version='0.0.3',
    packages=setuptools.find_packages(),
    url='https://github.com/DreamFaceAI/dream_api',
    license='MIT',
    author='DreamApi',
    description='DreamApi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)