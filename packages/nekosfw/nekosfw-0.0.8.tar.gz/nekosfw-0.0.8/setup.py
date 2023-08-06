from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

VERSION = '0.0.8'
DESCRIPTION = 'Get SFW Neko Images'
LONG_DESCRIPTION = 'A api wrapper that get links for SFW neko images and has a basic rate limit handler.'

# Setting up
setup(
    name="nekosfw",
    version=VERSION,
    author="Crain69 (Chirayu Prasai)",
    description=DESCRIPTION,
    author_email="<chirayuprasai11@gmail.com>",
    url="https://github.com/Neko-SFW/nekosfw-py",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['aiohttp'],
    keywords=['python', 'neko', 'sfw',
              'rate limit', 'handler', 'images'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
