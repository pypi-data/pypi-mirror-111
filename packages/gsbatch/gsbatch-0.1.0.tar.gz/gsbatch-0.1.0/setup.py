
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'gsbatch',
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Apply GhostScript to a batch of files',
    long_description = 'Apply GhostScript to a batch of files',
    keywords = 'YAML, Bash',
    url = 'https://github.com/tdegeus/gsbatch',
    packages = find_packages(),
    use_scm_version = {'write_to': 'gsbatch/_version.py'},
    setup_requires = ['setuptools_scm'],
    install_requires = ['click'],
    entry_points = {
        'console_scripts': [
            'gsbatch_topng = gsbatch.cli.gsbatch_topng:main',
        ]})
