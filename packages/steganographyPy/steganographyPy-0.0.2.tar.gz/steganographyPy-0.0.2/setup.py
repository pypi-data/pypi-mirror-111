from setuptools import setup, find_packages
import numpy as np


VERSION = '0.0.2'
DESCRIPTION = 'Encodes text into image'
LONG_DESCRIPTION = 'Encodes text into image given as numpy array.'

# Setting up
setup(
    name="steganographyPy",
    version=VERSION,
    author="Kryzma",
    author_email="<gramolis1@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'steganography'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
