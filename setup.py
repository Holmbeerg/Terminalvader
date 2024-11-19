from setuptools import setup, find_packages

setup(
    name="smhi",
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'ujson',
        'tzlocal',
        'requests',
    ],
    entry_points = {
        'console_scripts': [
            'smhi = src.smhi:main',
        ],
    }
)
