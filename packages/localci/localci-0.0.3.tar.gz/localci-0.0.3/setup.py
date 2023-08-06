from setuptools import setup
from localci.version import __version__

setup(
    name='localci',
    description='Makes local CI with Python, npm, and Java easy. Integrated with custom docker registry.',
    version=__version__,
    packages=['localci'],
    install_requires=[
        'rich', 'pyfiglet'
    ],
    python_requires='>=3.8',
    entry_points='''
        [console_scripts]
        localci=localci.__main__:main
    '''
)
