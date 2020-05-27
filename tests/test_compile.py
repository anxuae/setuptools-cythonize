# -*- coding: utf-8 -*-

import sys
import fnmatch
import os.path as osp
from wheel_inspect import inspect_wheel


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


def test_no_compile(testdir):

    setup_file = make_setup(testdir)

    # Run all tests with pytest
    result = testdir.run(sys.executable, setup_file, 'bdist')
    assert result.ret == 0

    for path in testdir.tmpdir.join('dist').listdir():
        assert path.fnmatch('spam-0.0.0-py*-none-any.whl')

        output = inspect_wheel(str(path))
        assert output["dist_info"]["wheel"]["root_is_purelib"]

        files = [r["path"] for r in output["dist_info"]["record"] if r["path"].startswith("spam/")]
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

    for path in testdir.tmpdir.join('dist').listdir():
        assert path.fnmatch('spam-0.0.0-cp*-cp*m-*.whl')

        output = inspect_wheel(str(path))
        assert not output["dist_info"]["wheel"]["root_is_purelib"]

        files = [r["path"] for r in output["dist_info"]["record"] if r["path"].startswith("spam/")]
        assert osp.join('spam', '__init__.py') in files
        assert not osp.join('spam', '__main__.py') in files
        assert fnmatch.filter(files, osp.join('spam', '__main__*.so'))
        assert not osp.join('spam', 'ham.py') in files
        assert fnmatch.filter(files, osp.join('spam', 'ham*.so'))
        assert osp.join('spam', 'egg', '__init__.py') in files
        assert not osp.join('spam', 'egg', 'bean.py') in files
        assert fnmatch.filter(files, osp.join('spam', 'egg', 'bean*.so'))
        assert osp.join('spam', 'egg', 'sausage.py') in files
