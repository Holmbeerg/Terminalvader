from setuptools import setup, find_packages

setup(
    name="smhi",
    version='1.0',
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'smhi = src.smhi:main',
        ],
    }
)