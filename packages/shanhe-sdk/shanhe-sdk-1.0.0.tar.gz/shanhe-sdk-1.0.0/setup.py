# coding:utf-8

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 6):
    error = 'ERROR: shanhe-sdk requires Python Version 2.6 or above.'
    print >> sys.stderr, error
    sys.exit(1)


setup(
    name='shanhe-sdk',
    version='1.0.0',
    description='Software Development Kit for ShanHe.',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    keywords='shanhe iaas OIS sdk',
    author='ShanHe Team',
    author_email='zhaoshsh@jnist.cn',
    url='https://docsv3.shanhe.com/development_docs/sdk/',
    packages=['shanhe', 'shanhe.conn', 'shanhe.iaas', 'shanhe.iaas.actions',
              'shanhe.misc', 'shanhe.ois'],
    package_dir={'shanhe-sdk': 'shanhe'},
    namespace_packages=['shanhe'],
    include_package_data=True,
    install_requires=['future']
)
