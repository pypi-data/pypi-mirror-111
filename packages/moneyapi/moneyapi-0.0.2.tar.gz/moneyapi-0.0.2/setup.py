from setuptools import setup, find_packages
import codecs
import os

current = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(current, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'This is the moneyapi http request package.'

# Setting up
setup(
    name="moneyapi",
    version=VERSION,
    author="Mason Worthen",
    author_email="datalockhostingllc@gmail.com",
    description=DESCRIPTION,

    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'moneyapi', 'API', 'financial'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
