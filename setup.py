#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name="django-doberman",
    version="0.1.0",
    author="Nicolas Mendoza",
    author_email="niccolasmendoza@gmail.com",
    maintainer='Nicolas Mendoza',
    maintainer_email='niccolasmendoza@gmail.com',
    description="Django app that locks out users after too many failed login attempts.",
    long_description=open('README.rst').read(),
    license="MIT License",
    keywords="django locks users account login attempts banned ip doberman authentication",
    url="https://github.com/nicchub/django-doberman",
    packages=[
        'doberman'
    ],
    include_package_data=True,
    tests_require=['python-coveralls'],
    install_requires=[
        'Django>=1.7.0'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"
    ]
)