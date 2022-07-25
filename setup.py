from setuptools import find_packages, setup

setup(
    name='password manager',
    version='1.0.0',
    packages=[
        'click'
    ],
    entry_points={
        'console_scripts': [
            'pman=manager:cli'
        ]
    }
)
