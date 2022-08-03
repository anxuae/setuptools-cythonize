# -*- coding: utf-8 -*-

"""
Distribute python modules/packages as binary files (compilation based on Cython)
"""

import sys
from fnmatch import fnmatchcase
from distutils.dist import Distribution
from distutils.command.build import build
from distutils.command.bdist import bdist

from setuptools.command.build_py import build_py
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext

from wheel.bdist_wheel import bdist_wheel

from Cython.Distutils import Extension


__version__ = "1.0.6"


class CythonizeBuild(build, object):  # 'object' inheritance permits @property usage

    """
    This patch ensure that extension will be built even if there
    is no extension declared in the setup.
    """

    _use_cython = None

    user_options = build.user_options + [('cythonize', None, 'compile pure python file using cython')]
    boolean_options = build.boolean_options + ['cythonize']

    @property
    def cythonize(self):
        return self._use_cython

    @cythonize.setter
    def cythonize(self, value):
        self._use_cython = value
        if self._use_cython:
            self.distribution.has_ext_modules = lambda: True
        else:
            self.distribution.has_ext_modules = lambda: Distribution.has_ext_modules(self.distribution)

    def initialize_options(self):
        build.initialize_options(self)
        self.cythonize = None

    def finalize_options(self):
        build.finalize_options(self)


class CythonizeBuildPy(build_py):

    """
    This patch moves python files from build_py to build_ext (handled by Cython)
    except __init__.py to keep Python package integrity.
    """

    user_options = build.user_options + [('cythonize', None, 'compile pure python file using cython')]
    boolean_options = build.boolean_options + ['cythonize']

    def initialize_options(self):
        build_py.initialize_options(self)
        self.cythonize = None
        self.exclude_cythonize = []

    def finalize_options(self):
        build_py.finalize_options(self)
        self.set_undefined_options('build', ('cythonize', 'cythonize'))

        if self.cythonize:
            self.compile = self.optimize = False  # noqa

    def run(self):
        if self.cythonize:
            # Move py files to ext_modules except __init__.py
            if not self.distribution.ext_modules:
                self.distribution.ext_modules = []
            for (pkg, mod, pth) in build_py.find_all_modules(self):
                if self.is_to_cythonize(pkg, mod):
                    self.distribution.ext_modules.append(
                        Extension(
                            ".".join([pkg, mod]),
                            [pth],
                            cython_c_in_temp=True,
                            # Ensure cython compiles with a relevent language mode setting
                            cython_directives={'language_level': sys.version[0]}
                        )
                    )
        return build_py.run(self)

    def find_all_modules(self):
        """List all modules that have to be kept in pure Python.
        """
        return [(pkg, mod, pth) for pkg, mod, pth in build_py.find_all_modules(self)
                if not self.is_to_cythonize(pkg, mod)]

    def build_module(self, module_name, module_file, package_name):
        if self.is_to_cythonize(package_name, module_name):
            return
        return build_py.build_module(self, module_name, module_file, package_name)

    def is_to_cythonize(self, package_name, module_name):
        """Return True if the given module has to be compiled.
        """
        if not self.cythonize:
            return False

        cythonize = True
        if self.exclude_cythonize:
            pkgmod = '.'.join([package_name, module_name])
            for pat in self.exclude_cythonize:
                if fnmatchcase(pkgmod, pat):
                    cythonize = False
        return cythonize and module_name not in ['__init__', '__main__']


class CythonizeInstall(install):

    """
    This patch add the option :option:`--cythonize` to the install
    command
    """

    user_options = install.user_options + [('cythonize', None, 'compile pure python file using cython')]
    boolean_options = install.boolean_options + ['cythonize']

    def initialize_options(self):
        install.initialize_options(self)
        self.cythonize = None

    def finalize_options(self):
        install.finalize_options(self)
        # Pass option to the build command
        build_cmd = self.get_finalized_command('build')
        if build_cmd.cythonize is None:
            build_cmd.cythonize = self.cythonize

    def run(self):
        # It seems absurd, but doing that force setuptools to execute the
        # old-style "install" command instead of the "egg_install" one.
        # This is due to frame inspection in setuptools.command.install.install.run()
        install.run(self)


class CythonizeBdist(bdist):

    """
    This patch add the option :option:`--cythonize` to the bdist
    command and configure 'wheel' as default format.
    """

    user_options = bdist.user_options + [('cythonize', None, 'compile pure python file using cython')]
    boolean_options = bdist.boolean_options + ['cythonize']

    @classmethod
    def set_default_wheel_format(cls):
        """Set 'wheel' as default format.
        """
        if "wheel" not in cls.format_commands:
            cls.format_commands['wheel'] = ('bdist_wheel', "Python .whl file")
            for keyos in cls.default_format:
                cls.default_format[keyos] = 'wheel'

    def initialize_options(self):
        bdist.initialize_options(self)
        self.cythonize = None

    def finalize_options(self):
        bdist.finalize_options(self)
        # Pass option to the build command
        build_cmd = self.get_finalized_command('build')
        if build_cmd.cythonize is None:
            build_cmd.cythonize = self.cythonize


class CythonizeBdistWheel(bdist_wheel):

    """
    This patch add the option :option:`--cythonize` to the bdist_wheel
    command.
    """

    user_options = bdist_wheel.user_options + [('cythonize', None, 'compile pure python file using cython')]
    boolean_options = bdist_wheel.boolean_options + ['cythonize']

    def initialize_options(self):
        bdist_wheel.initialize_options(self)
        self.cythonize = None

    def finalize_options(self):
        """
        Prepare the build command (do it before 'bdist_wheel' to patch
        the detection of C-compiled sources)
        """
        build_cmd = self.get_finalized_command('build')
        if build_cmd.cythonize is None:
            build_cmd.cythonize = self.cythonize
        bdist_wheel.finalize_options(self)


def get_cmdclass(wheel_default=True):

    if wheel_default:
        CythonizeBdist.set_default_wheel_format()

    return {'build': CythonizeBuild,
            'build_py': CythonizeBuildPy,
            'build_ext': build_ext,
            'bdist': CythonizeBdist,
            'bdist_wheel': CythonizeBdistWheel,
            'install': CythonizeInstall}
