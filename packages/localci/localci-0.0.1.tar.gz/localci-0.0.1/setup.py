from setuptools import setup

setup(
    name='localci',
    description='Makes local CI with Python, npm, and Java easy. Integrated with custom docker registry.',
    version='0.0.1',
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
