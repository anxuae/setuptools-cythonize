# -*- coding: utf-8 -*-

import sys
import fnmatch
import zipfile
import os.path as osp
from py.path import local


def make_setup(testdir):
    """Create a temporary directory and copy the 'spam' package"""

    setup_file = testdir.makepyfile("""

    from setuptools import setup
    from setuptools_cythonize import get_cmdclass

    setup(cmdclass=get_cmdclass(),
          name='spam',
          packages=['spam', 'spam.egg'],
          options={
              'build_py':
                  {'exclude_cythonize': ['spam.egg.sau*']}
          },
        )

    """)

    # Copy test package
    spam_dir = testdir.request.config.rootdir.join('tests', 'spam')
    spam_dir.copy(testdir.tmpdir.join('spam'))

    return setup_file


def find_wheel(dirname, pattern='*.whl'):
    """Return a wheel file matching the given pattern in the directory."""
    if isinstance(dirname, str):
        dirname = local(dirname)

    for path in dirname.listdir():
        if path.fnmatch(pattern):
            return path


def list_wheel(wheel_file):
    """Return the list of file in the wheel."""
    return [f.filename for f in zipfile.ZipFile(str(wheel_file)).filelist if f.filename.startswith("spam/")]


def test_no_compile(testdir):

    setup_file = make_setup(testdir)

    # Run all tests with pytest
    result = testdir.run(sys.executable, setup_file, 'bdist')
    assert result.ret == 0

    wheel_file = find_wheel(testdir.tmpdir.join('dist'), 'spam-0.0.0-py*-none-any.whl')
    assert wheel_file

    files = list_wheel(wheel_file)
    assert osp.join('spam', '__init__.py') in files
    assert osp.join('spam', '__main__.py') in files
    assert osp.join('spam', 'ham.py') in files
    assert osp.join('spam', 'egg', '__init__.py') in files
    assert osp.join('spam', 'egg', 'bean.py') in files
    assert osp.join('spam', 'egg', 'sausage.py') in files


def test_compile(testdir):

    setup_file = make_setup(testdir)

    # Run all tests with pytest
    result = testdir.run(sys.executable, setup_file, 'bdist', '--cythonize')
    assert result.ret == 0

    wheel_file = find_wheel(testdir.tmpdir.join('dist'), 'spam-0.0.0-cp*-cp*m*.whl')
    assert wheel_file

    files = list_wheel(wheel_file)
    assert osp.join('spam', '__init__.py') in files
    assert osp.join('spam', '__main__.py') in files
    assert not osp.join('spam', 'ham.py') in files
    assert fnmatch.filter(files, osp.join('spam', 'ham*.so'))
    assert osp.join('spam', 'egg', '__init__.py') in files
    assert not osp.join('spam', 'egg', 'bean.py') in files
    assert fnmatch.filter(files, osp.join('spam', 'egg', 'bean*.so'))
    assert osp.join('spam', 'egg', 'sausage.py') in files
