from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Quiffen'
with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="quiffen",
    version='0.1.1',
    author="Isaac Harris-Holt",
    author_email="isaac@harris-holt.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    install_requires=[],
    keywords=['qif'],
    license='GNU GPLv3',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3'
)
