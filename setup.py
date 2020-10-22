from setuptools import setup, find_packages

def get_version(rel_path):
    with open(rel_path, 'r') as f:
        for line in f.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="CA Visual Fingerprinter",
    version=get_version('cafingerprinter/__init__.py'),
    author="Ben Klein",
    author_email="bklein3@vols.utk.edu,robobenklein@gmail.com",
    description="Part of the CodeAnalytics suite for generic code analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/utk-se/CodeAnalytics-visualfingerprinter",
    packages=find_packages(),
    install_requires=[
        "ca-distributor @ git+ssh://git@github.com/utk-se/CodeAnalytics-distributor.git#egg=ca-distributor",
        "numpy"
    ],
    dependency_links = [
        'http://github.com/utk-se/CodeAnalytics-distributor/tarball/master#egg=ca-distributor'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
          'ca-fingerprinter=cafingerprinter:main'
        ]
    },
    python_requires='>=3.6',
)
