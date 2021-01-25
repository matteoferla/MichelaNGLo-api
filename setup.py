########################################################################################################################
__doc__ = \
    """
    Pip install file. All the files have this block here, so in PyCharm I can change them en-mass.
    """

__author__ = "Matteo Ferla. [Github](https://github.com/matteoferla)"
__email__ = "matteo.ferla@gmail.com"
__date__ = "10 July 2020 A.D."
__license__ = "MIT"
__version__ = "1.1.1"
__citation__ = "None."

########################################################################################################################


from setuptools import setup, find_packages

import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='michelanglo_api',
    version= __version__,
    packages=find_packages(),
    url='https://github.com/matteoferla/MichelaNGLo-api',
    license=__license__,
    author=__author__,
    author_email=__email__ ,
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='API to interface with Michelanglo'
)
