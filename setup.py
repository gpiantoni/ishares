from setuptools import setup, find_packages

VERSION = '0.1'

long_description = ''

setup(
    name='ishares',
    version=VERSION,
    description='',
    long_description=long_description,
    url='https://github.com/gpiantoni/ishares',
    author="Gio Piantoni",
    author_email='ishares@gpiantoni.com',
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
