'''
Author: 龙嘉伟
Date: 2021-06-28 19:10:40
LastEditors: 龙嘉伟
LastEditTime: 2021-07-01 15:12:48
Description: 
'''
#! -*- coding: utf-8 -*-
import os
import shutil
import sys

from pkg_resources import DistributionNotFound, get_distribution
from setuptools import find_packages, setup

stdout = sys.stdout
stderr = sys.stderr

log_file = open('setup.log', 'w')
sys.stdout = log_file
sys.stderr = log_file

with open('README.md', 'r', encoding = 'utf8') as fh:
    long_description = fh.read()

setup(
    name='polypoly',
    version='0.0.3',
    description='Chinese polyphone model',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/ljv006/polypoly',
    author='ljv006',
    author_email='longjw6@qq.com',
    classifiers = [
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    # include_package_data = True,
    packages=['polypoly'],
    package_dir = {'polypoly':'polypoly'},
    install_requires=['tensorflow>=2.0.0', 'pypinyin', 'jieba'],
    package_data= {"polypoly":["__init__.py", "data/*", 'ckpts/*', 'ckpts/eval/*', 'ckpts/.data-00000-of-00001', 'ckpts/.index', 'ckpts/.meta', 'savedModel/variables/*', 'savedModel/saved_model.pb']},
    python_requires='>=3.6',
)
log_file.close()

sys.stdout = stdout
sys.stderr = stderr

with open('setup.log', 'r') as log_file:
    sys.stdout.write(log_file.read())
