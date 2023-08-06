# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/6/25 16:58
Desc: XHData's pypi info file
"""
import re
import ast

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open('requirements.txt') as reqs_file:
    INSTALL_REQUIRES = reqs_file.readlines()


def get_version_string():
    """
    Get the XHData version number
    :return: version number
    :rtype: str, e.g. '0.1.1'
    """
    with open("xhdata/__init__.py", "rb") as _f:
        version_line = re.search(
            r"__version__\s+=\s+(.*)", _f.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


setuptools.setup(
    name="xhdata",
    version=get_version_string(),
    author="xh",
    author_email="admin@xuheen.com",
    license="MIT",
    description="XhData is an elegant and simple financial data interface library for Python, built for human beings!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'xhdata=xhdata.Command:command',
            'xhdata-tdx=xhdata.Command:Tdx',
            'xhdata-tushare=xhdata.Command:Tushare',
            'xhdata-akshare=xhdata.Command:AKShare',
        ]
    },
    package_data={"": ["*.py", "*.json", "*.pk", "*.js"]},
    keywords=[
        "stock",
        "quant",
        "data"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
