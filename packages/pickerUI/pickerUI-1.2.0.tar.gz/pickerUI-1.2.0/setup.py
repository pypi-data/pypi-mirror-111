# -*- encoding: utf-8 -*-
"""
@File    : setup.py
@Time    : 2021/7/1 5:19 下午
@Author  : Jiaoxuewei
@Email   : jovae@qq.com
"""
import os
from setuptools import setup, find_packages

def fread(fname):
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath, 'r') as fp:
        return fp.read()
setup(
    name = 'pickerUI',
    version = '1.2.0',
    keywords='pickerUI',
    description = 'a library of menu ui',
    long_description=fread('README.rst'),
    license = 'MIT License',
    url = 'https://github.com/mlpod/pickerUI',
    author = 'Jiaoxuewei',
    author_email = 'jovae@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any'
)