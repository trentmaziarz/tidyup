from setuptools import setup, find_packages

setup(
    name='tidyup',
    version='0.2.1',
    description='Sort a downloads folder by rules in a YAML file',
    author='Trent Maziarz',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['PyYAML', 'click>=7.0'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['tidyup = tidyup.cli:main'],
    },
)
