# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sched_data_interface',
    version='0.1.0',
    description='This module handles the retreival of Sched.com session/user data to be consumed by other Connect Automation scripts.',
    long_description=readme,
    author='Kyle Kirkby',
    author_email='kyle.kirkby@linaro.org',
    url='https://github.com/linaro-marketing/SchedDataInterface',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
