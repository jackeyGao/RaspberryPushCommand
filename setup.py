# -*- coding: utf-8 -*-
'''
File Name: steup.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 2015年07月13日 星期一 13时02分21秒
'''

from setuptools import setup, find_packages

version = "0.2"
description = "https://github.com/jackeyGao/RaspberryPushCommand"


def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()

setup(
    name='RaspberryPushCommand',
    version=version,
    install_requires=[
        'pushbullet.py',
        'requests',
    ],
    zip_safe=False,
    py_modules = ['server', 'cmd'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'listener = server:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    license="MIT",
    description=description,
    long_description=fread('README.md'),
    author='JackeyGao',
    author_email='oommmme@gmail.com',
    url='https://github.com/jackeygao/RaspberryPushCommand',
)


