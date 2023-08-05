#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Kristian Bonnici",
    author_email='kristiandaaniel@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="MLVizLib is a powerful package for generating quick, insightful, and stylish visualizations for machine learning.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mlvizlib',
    name='mlvizlib',
    packages=find_packages(include=['mlvizlib', 'mlvizlib.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kristianbonnici/mlvizlib',
    version='0.0.4',
    zip_safe=False
)
