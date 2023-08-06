import os
from subprocess import check_output, CalledProcessError
from setuptools import setup

setup(
    name = "dobro",
    version = "0.4.2",
    author = "Doug Thompson",
    author_email = "s-git@dougthompson.co.uk",
    description = ("[DEPRECATED] Manage DigitalOcean droplets by tag"),
    license = "MIT",
    keywords = "digitalocean droplet cli doctl devops",
    url = "https://gitlab.com/snoopdouglas/dobro",
    packages=['dobro'],
    entry_points = {
        'console_scripts': ['dobro=dobro.cli:main'],
    },
    long_description="[DEPRECATED] Manage DigitalOcean droplets by tag. This is unmaintained.",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Development Status :: 7 - Inactive",
        "Topic :: Utilities",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ],
    test_suite='dobro.tests',
    zip_safe=False,
)
