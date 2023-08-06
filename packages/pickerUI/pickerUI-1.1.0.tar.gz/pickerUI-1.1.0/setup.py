# -*- encoding: utf-8 -*-
"""
@File    : setup.py
@Time    : 2021/7/1 5:19 下午
@Author  : Jiaoxuewei
@Email   : jovae@qq.com
"""

from setuptools import setup, find_packages

setup(
    name = 'pickerUI',
    version = '1.1.0',
    keywords='pickerUI',
    description = 'a library of menu ui',
    license = 'MIT License',
    url = 'https://github.com/mlpod/pickerUI',
    author = 'Jiaoxuewei',
    author_email = 'jovae@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any'
)