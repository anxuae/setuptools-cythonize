

The ``setuptools-cythonize`` project attempts to provide ``distutils`` commands
to compile **Python** code into **C** code using ``Cython``. The generated code
is packaged into a platform dependent archive.

Install
-------

::

     $> sudo pip install setuptools-cythonize


Setup configuration
-------------------

Add the ``cmdclass`` keyword to the setup:

.. code-block:: python

    from setuptools_cythonize import get_cmdclass

    setup(
        cmdclass=get_cmdclass(),
        name="my_package",
        version="2.0.5",
        description="My custom library",
        ...
    )

.. note:: the function ``get_cmdclass()`` force **wheel** as default format
          (recommended format for binary distribution). This behavior can be
          disabled by setting ``wheel_default=False``.

Some packages can be excluded from the *cythonization* by setting the ``exclude_cythonize``
option. The module matching is done using the function
`fnmatch.fnmatchcase <https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatchcase>`_ .

.. code-block:: python

    setup(
        cmdclass=get_cmdclass(),
        name="my_package",
        ...
        options={
            'build_py':
                {'exclude_cythonize': ['my_package.subpack*']}
        },
        ...
    )

Packaging
---------

Call the ``setup.py`` file to generate the package, all Python modules
(except the ones defined in ``exclude_cythonize``) will be compiled
and packaged::

     $> python setup.py bdist --cythonize
