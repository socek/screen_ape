from setuptools import find_packages
from setuptools import setup

setup(
    name="Screen Ape",
    version="0.1",
    description="",
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    long_description=__doc__,
    author='Dominik "Socek" Długajczyk',
    author_email="msocek@gmail.com",
    license="MIT",
    zip_safe=False,
    url="http://github.com/socek/screen_ape",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
