========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pwcheck/badge/?style=flat
    :target: https://pwcheck.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/Itotutona/pwcheck.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/Itotutona/pwcheck

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/Itotutona/pwcheck?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/Itotutona/pwcheck

.. |requires| image:: https://requires.io/github/Itotutona/pwcheck/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Itotutona/pwcheck/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/Itotutona/pwcheck/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Itotutona/pwcheck

.. |version| image:: https://img.shields.io/pypi/v/pwcheck.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pwcheck

.. |wheel| image:: https://img.shields.io/pypi/wheel/pwcheck.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pwcheck

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pwcheck.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pwcheck

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pwcheck.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pwcheck

.. |commits-since| image:: https://img.shields.io/github/commits-since/Itotutona/pwcheck/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/Itotutona/pwcheck/compare/v0.1.0...master



.. end-badges

Python Password Checker

* Free software: GNU Lesser General Public License v3 (LGPLv3)

Installation
============

::

    pip install pwcheck

You can also install the in-development version with::

    pip install https://github.com/Itotutona/pwcheck/archive/master.zip


Documentation
=============


https://pwcheck.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
