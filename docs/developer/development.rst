Development
===========

Use ``main`` for everyday development. Keep changes small; short-lived branches
are useful for review, while releases are identified by version tags.

Current environment
-------------------

Install uv using its `installation guide
<https://docs.astral.sh/uv/getting-started/installation/>`__, then run from a
checkout::

    uv venv --python 3.15 .venv
    source .venv/bin/activate
    uv pip install --upgrade -e ".[dev,docs]"
    .venv/bin/pre-commit install

The development environment uses Python 3.15 and the newest compatible package
versions. Runtime dependencies have no upper bounds. No lockfile constrains
local upgrades. To refresh the environment, repeat ``uv pip install --upgrade``.
Python 3.12 through 3.15 are checked in CI; supporting older Python versions
does not require using them for development.

Native build prerequisites
--------------------------

PySHTOOLS provides native code. When a wheel is unavailable for a new Python
version, install a Fortran compiler, FFTW, BLAS/LAPACK and pkg-config before
creating the environment. On Ubuntu::

    sudo apt-get update
    sudo apt-get install gfortran libfftw3-dev libopenblas-dev pkg-config

On Arch Linux, the corresponding packages include ``gcc-fortran``, ``fftw``,
``blas``, ``lapack`` and ``pkgconf``. CI and Read the Docs declare the Ubuntu
build dependencies explicitly. Older Python versions may install a wheel and
avoid this source-build step.

Checks
------

Run from the repository root::

    .venv/bin/ruff check .
    .venv/bin/ruff format --check .
    .venv/bin/python -m pytest
    .venv/bin/python -m sphinx -W --keep-going -b html docs docs/_build/html
    .venv/bin/python -m build
    .venv/bin/twine check --strict dist/*
    .venv/bin/check-wheel-contents dist/*.whl
    .venv/bin/python -m unittest discover -s .github/scripts/tests -v

To validate citation metadata without constraining the project environment::

    uvx --python 3.15 cffconvert --validate

CI runs on pushes to ``main``, pull requests, manual requests and a weekly
schedule. Each run resolves current dependencies. It checks citation metadata,
lint, documentation, all supported Python versions and both installed
artifacts. Coverage and rendered documentation are retained as run artifacts.
The Release workflow reuses these same checks before publishing.

Read the Docs uses the root ``.readthedocs.yaml``. Repository, default branch
and webhook settings must also match the project; see the release guide for
account setup.
