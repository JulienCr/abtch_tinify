from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='batch_tinify',
    version='0.1',
    py_modules=['batch_tinify'],
    entry_points={
        'console_scripts': [
            'batch_tinify=main:main',
        ],
    },
)
