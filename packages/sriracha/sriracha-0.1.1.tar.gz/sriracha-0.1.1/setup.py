from setuptools import setup, find_packages

# load readme
with open('readme.md', 'r') as file:
    readme = file.read()

setup(
    name='sriracha',
    version='0.1.1',
    description='MVC Web Framework',

    long_description=readme,
    long_description_content_type='text/markdown',

    author='pcranaway',
    author_email='pcranaway@tuta.io',

    packages=find_packages(),

    install_requires=['python-liquid', 'click', 'GitPython'],

    entry_points={
        'console_scripts': [
            'sri=sri:main'
        ]
    },

    license='GPL',
    license_file='LICENSE'
)
