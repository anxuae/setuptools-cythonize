# -*- coding: utf-8 -*-

from setuptools_cythonize import get_cmdclass


def test_call():
    classes = get_cmdclass()
    assert 'build_py' in classes
    assert 'build' in classes
    assert 'build_py' in classes
    assert 'build_ext' in classes
    assert 'bdist' in classes
    assert 'bdist_wheel' in classes
    assert 'install' in classes
