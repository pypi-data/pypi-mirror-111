from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'tool for managing configuration profiles'
LONG_DESCRIPTION = ''

setup(
    name="poket",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="pnowk",
    author_email="pnowk123@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'twine', 
        'wheel',
        'python-dotenv',
        'black',
        'bumpversion',
        'pytest'
    ],
    keywords='python',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)