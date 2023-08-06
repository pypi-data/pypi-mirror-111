import os
from celtis.Config import __version__
from setuptools import setup, find_packages

try:
    from pypandoc import convert_file
    read_md = lambda f: convert_file(f, 'rst', 'md')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name = "celtis",
    version = __version__,
    author = "Vikrant Singh Chauhan",
    author_email = "vi@hackberry.xyz",
    description = ("Modern scriptable Vulnerability Scanner"),
    license = "MIT",
    keywords = ("penetration testing", "hacking", "vulnerability scanner"),
    url = "http://github.com/0xcrypto/celtis",
    long_description=read_md('README.md'),
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'click',
    ],
    entry_points = {
        'console_scripts': ['celtis=celtis:cli'],
    }
)
