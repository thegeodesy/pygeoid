.. _install:

Installing
==========

Installing a release
--------------------

You can install ``pygeoid`` using the `pip package manager
<https://pypi.org/project/pip/>`__::

    python -m pip install pygeoid


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest version of the source code from
GitHub::

    python -m pip install --upgrade "git+https://github.com/thegeodesy/pygeoid@main"

The development branch requires Python 3.12 or newer. Released versions can
have different Python requirements; pip selects a compatible release.
Development APIs can change between minor versions.

For an editable checkout::

    git clone --branch main https://github.com/thegeodesy/pygeoid.git
    cd pygeoid
    uv venv --python 3.15 .venv
    source .venv/bin/activate
    uv pip install --upgrade -e .

For Python 3.15, PySHTOOLS may need a Fortran source build; see the native
build prerequisites in :doc:`developer/development`.

See :doc:`developer/development` for testing and documentation commands.
