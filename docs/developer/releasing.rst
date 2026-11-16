Releases and integrations
=========================

Release cycle
-------------

Develop on ``main`` and release small, tested changes frequently. Version tags
retain access to older releases; a permanent development branch is not required.
Use a new version for every release, including fixes to a published package.

After CI is green on the chosen commit::

    git pull --ff-only
    gh release create vX.Y.Z --target main --generate-notes

Replace ``vX.Y.Z`` with the intended version. To prepare notes without publishing,
add ``--draft``. Publishing the GitHub release triggers ``release.yml``.
Pre-release tags such as ``vX.Y.Zrc1`` are also supported; mark the GitHub release
as a pre-release to make its status clear.

The workflow verifies the tag belongs to ``main``, runs the shared checks,
builds a wheel and source distribution, validates their names and versions,
and tests each in a clean environment outside the checkout. PyPI receives those
same tested artifacts. They are then attached to the GitHub release.
Setuptools-scm derives the package version from Git; no manual version file edit
is needed. Published/shared history should not be rewritten to clean up commits.

Run the Release workflow manually from GitHub Actions to rehearse the complete
checks without publishing to PyPI or creating a release. Manual runs do not
receive publishing credentials. No release is created by an ordinary push to
``main``.

PyPI setup (once per project)
-----------------------------

In the existing PyPI project's Publishing settings, add a GitHub Trusted
Publisher with these exact values:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Value
   * - Owner
     - ``thegeodesy``
   * - Repository
     - ``pygeoid``
   * - Workflow filename
     - ``release.yml``
   * - Environment
     - ``pypi``

Publishing settings:
https://pypi.org/manage/project/pygeoid/settings/publishing/

The GitHub ``pypi`` environment is restricted to version tags matching ``v*``.
The publish job uses a short-lived OIDC credential; no PyPI token is stored in
GitHub secrets. Creating the workflow or environment does not register the
publisher on PyPI. The account-side registration must be completed before the
first automated publication.

Read the Docs setup
-------------------

In the existing project settings:

* Set repository URL to ``https://github.com/thegeodesy/pygeoid.git``.
* Set the default branch to ``main`` and configuration file to
  ``.readthedocs.yaml``.
* Resynchronize repository versions, activate ``main`` and point ``latest`` at
  the default branch. Keep release versions available as appropriate.
* Reconnect the GitHub integration or copy the newly generated webhook details
  to GitHub; retain the old webhook until a new delivery succeeds.
* Trigger a ``main`` build and verify the existing documentation domain.

A configuration file cannot repair a stale webhook token or service-side
repository association by itself. Do not expose webhook URLs/tokens in issues,
logs or committed configuration.

Citation and archiving
----------------------

``CITATION.cff`` supplies GitHub's citation menu and is validated in CI.
``.zenodo.json`` supplies metadata for Zenodo release archives. In Zenodo's
GitHub settings, resynchronize repositories and enable this transferred
repository for archiving. Confirm the existing DOI association before enabling
an existing project under a new repository owner. Do not create a replacement
DOI series for an already archived project.

PyGeoid retains the concept DOI ``10.5281/zenodo.4692429``.

External services
-----------------

The GitHub Actions artifacts provide test coverage and built documentation.
Legacy Travis, Codacy, Scrutinizer and other webhook integrations are independent
of CI. Retire only services no longer in use, after checking their account-side
settings. A successful CI run does not prove that external webhooks or DOI
registration work.
