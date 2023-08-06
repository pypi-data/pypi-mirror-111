from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Random word generator'
LONG_DESCRIPTION = '''Generates a random word from a list of over 6000 commonly used nouns from http://www.desiquintans.com/nounlist.  
Installation  
pip install get-random-word  
Usage  
from get-random-word import get_random  '''


# Setting up
setup(
    name="get_random_word",
    version=VERSION,
    author="Kunal Ostwal",
    author_email="<kunaldostwal@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'random word generator', 'random noun generator'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
