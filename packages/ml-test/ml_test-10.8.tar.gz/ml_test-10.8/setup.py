#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/1 3:15 下午
# @Author : hehao1
# @Site : 
# @File : setup.py
# @Software: PyCharm
from setuptools import setup, find_packages

setup(
    setup_requires=['pbr'],
    name="ml_test",
    version="10.8",
    author="xxxxes",
    author_email="291073454@qq.com",
    description="Learn to Pack Python Module",
    # 项目主页
    #url="http://",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    #packages=find_packages(),

    #
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # 该文件入口指向 foo/main.py 的main 函数
    #entry_points={
    #   'console_scripts': [
    #        'project_init_test = project_init_test.create_new_demo:main'
    #    ]
    #},
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    
    package_data={'src/MONKEY/project_init/':['*.conf','project_init.md']
               },
               
    data_files=[('lib/python3.6/site-packages/MONKEY/project_init/',['package_test/src/MONKEY/project_init/*.conf','package_test/src/MONKEY/project_init/project_init.md']),
                ('lib/python3.6/site-packages/MONKEY/config/',['package_test/config/*'])]

)
