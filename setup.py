from setuptools import setup, find_packages

setup(
    name="facturapp",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'facturapp=facturapp.main:main',
        ],
    },
)