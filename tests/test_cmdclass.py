# -*- coding: utf-8 -*-

from setuptools_cythonize import get_cmdclass


def test_call():
    classes = get_cmdclass()
    assert 'build_py' in classes
