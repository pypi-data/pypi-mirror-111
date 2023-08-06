# -*- coding: utf-8 -*-
"""
    flask_githubcard
    ~~~~~~~~~~~~~

    :author: Jiang Wei <qq804022023@gmail.com>
    :copyright: © 2021 Jiang Wei
    :license: Apache Software License, see LICENSE for more details.
"""

from setuptools import setup
from os import path
from codecs import open

basedir = path.abspath(path.dirname(__file__))

with open(path.join(basedir, 'README-EN.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-Githubcard',
    version='1.0.4',
    url='https://2dogz.cn',
    license='Apache Software License',
    author='jiangwei',
    author_email='qq804022023@gmail.com',
    description='Generator a github card for flask web application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['flask_githubcard'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask', 'Requests'],
    keywords='flask extension development',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
