#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup, find_packages, Extension


HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)
import setuptools_cythonize


def main():
    setup(
        name="setuptools-cythonize",
        version=setuptools_cythonize.__version__,
        description=setuptools_cythonize.__doc__.strip(),
        long_description=open(osp.join(HERE, 'README.rst'), encoding='utf-8').read(),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Natural Language :: English',
            'Topic :: System :: Installation/Setup',
        ],
        author="Antoine Rousseaux",
        url="https://github.com/anxuae/setuptools-cythonize",
        download_url="https://github.com/anxuae/setuptools-cythonize/archive/{}.tar.gz".format(
            setuptools_cythonize.__version__),
        license='MIT license',
        platforms=['unix', 'linux', 'darwin', 'win32'],
        keywords=[
            'setup',
            'install',
            'compilation',
        ],
        packages=find_packages(),
        ext_modules=[Extension('setuptools_cythonize.cycompat', [
                                osp.join('setuptools_cythonize', 'cycompat.c')])],
        install_requires=[
            'setuptools>=36.2.0',
            'wheel>=0.29.0',
            'cython>=0.25.2'
        ],
        options={
            'bdist_wheel':
                {'universal': True}
        },
        zip_safe=False,  # Don't install the lib as an .egg zipfile
    )


if __name__ == '__main__':
    main()
