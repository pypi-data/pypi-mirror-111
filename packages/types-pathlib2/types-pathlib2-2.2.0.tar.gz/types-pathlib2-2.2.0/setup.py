from setuptools import setup

name = "types-pathlib2"
description = "Typing stubs for pathlib2"
long_description = '''
## Typing stubs for pathlib2

This is a PEP 561 type stub package for the `pathlib2` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pathlib2`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pathlib2. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ff2b92f340b1a8981457603b76db07266f04ac36`.
'''.lstrip()

setup(name=name,
      version="2.2.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['pathlib2-python2-stubs'],
      package_data={'pathlib2-python2-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
