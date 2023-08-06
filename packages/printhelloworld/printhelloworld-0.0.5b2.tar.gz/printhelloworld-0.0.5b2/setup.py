from setuptools import setup, find_packages
VERSION = '0.0.5b2'
DESCRIPTION = 'prints hello world and user input'
LONG_DESCRIPTION = 'prints hello world and user input.'

# Setting up
setup(
    name="printhelloworld",
    version=VERSION,
    author="Advai Shiralkar",
    author_email="advaitshiralkar2@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['say-hi'],
    keywords=[''],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
