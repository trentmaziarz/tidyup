from setuptools import setup, find_packages

setup(
    name='tidyup',
    version='0.1.0',
    description='Sort a downloads folder by rules in a YAML file',
    author='Trent Maziarz',
    packages=find_packages(exclude=['tests']),
    install_requires=['PyYAML'],
    entry_points={
        'console_scripts': ['tidyup = tidyup.cli:main'],
    },
)
