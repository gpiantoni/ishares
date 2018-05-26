from setuptools import setup, find_packages

VERSION = '0.1'

long_description = ''

setup(
    name='wonambi',
    version=VERSION,
    description='Tools for EEG, ECoG, iEEG, especially for sleep',
    long_description=long_description,
    url='https://github.com/wonambi-python/wonambi',
    author="Gio Piantoni / Jordan O'Byrne",
    author_email='wonambi@gpiantoni.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='analysis',
    packages=find_packages(exclude=('test', )),
    install_requires=[
        'requests',
        'pandas',
        ],
    )
