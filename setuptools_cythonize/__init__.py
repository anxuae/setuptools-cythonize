# -*- coding: utf-8 -*-

"""
Distribute python modules/packages as binary files (compilation based on Cython)
"""

__version__ = "1.0.6"

from setuptools.command.build_ext import build_ext
from setuptools_cythonize.cmdclass import (CythonizeBuild, CythonizeBuildPy,
                                           CythonizeBdist, CythonizeBdistWheel,
                                           CythonizeInstall)


def get_cmdclass(wheel_default=True):

    if wheel_default:
        CythonizeBdist.set_default_wheel_format()

    return {'build': CythonizeBuild,
            'build_py': CythonizeBuildPy,
            'build_ext': build_ext,
            'bdist': CythonizeBdist,
            'bdist_wheel': CythonizeBdistWheel,
            'install': CythonizeInstall}
