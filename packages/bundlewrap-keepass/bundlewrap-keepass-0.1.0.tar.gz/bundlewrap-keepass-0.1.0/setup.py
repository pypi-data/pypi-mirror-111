from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="bundlewrap-keepass",
    version="0.1.0",
    description="Use Keepass passwords in your bundlewrap repo",
    author="Franziska Kunsmann",
    author_email="pypi@kunsmann.eu",
    license="GPLv3",
    py_modules=['bwkeepass'],
    keywords=["configuration", "config", "management"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Systems Administration",
    ],
    install_requires=[
        "bundlewrap >= 4.0.0",
        "pykeepass >= 4.0.0",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
