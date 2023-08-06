import pathlib

from setuptools import setup
from localci.version import __version__

HERE = pathlib.Path(__file__).parent
README = (HERE / 'readme.md').read_text()

setup(
    name='localci',
    description='Makes local CI with Python, npm, and Java easy. Integrated with custom docker registry.',
    version=__version__,
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    author='briccardo',
    author_email='rbiagini02@gmail.com',
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
