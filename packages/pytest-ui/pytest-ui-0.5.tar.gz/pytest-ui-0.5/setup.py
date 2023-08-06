from os import path
from setuptools import setup

from pytui.settings import VERSION

# Get long description from README.md
PROJECT_DIR = path.abspath(path.dirname(__file__))
with open(path.join(PROJECT_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytest-ui',
    description='Text User Interface for running python tests',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=VERSION,
    license='MIT',
    platforms=['linux', 'osx', 'win32'],
    packages=['pytui'],
    url='https://github.com/martinsmid/pytest-ui',
    author_email='martin.smid@gmail.com',
    author='Martin Smid',
    entry_points={
        'console_scripts': [
            'pytui = pytui.ui:main',
        ]
    },
    install_requires=[
        'future',
        'pytest',
        'tblib',
        'urwid',
        'click',
    ],
    tests_require=[
        'mock'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
