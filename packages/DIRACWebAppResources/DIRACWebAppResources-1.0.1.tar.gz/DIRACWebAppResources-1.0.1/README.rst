.. -*- mode: rst -*-

DIRACWebAppResources
====================

.. image:: https://badge.fury.io/py/DIRACWebAppResources.svg
    :target: https://badge.fury.io/py/DIRACWebAppResources

``DIRACWebAppResources`` contains static resources used by ``WebAppDIRAC``.
It primarily exists to reduce the size of ``WebAppDIRAC`` releases by avoiding the need to duplicate about 128MB (36MB compressed) of files between every release.
You likely don't need to know about this package and should read about `WebAppDIRAC <https://pypi.org/project/WebAppDIRAC/>`_ instead.

Changelog
~~~~~~~~~


1.0.0
^^^^^

* Switch back to using ``package_data`` instead of ``data_files`` for distributing assets

1.0.0 (based on ExtJS 6.2.0)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Initial release

Release procedure
~~~~~~~~~~~~~~~~~

New releases can be made by making the following steps:

1. Update the ``DIRACWebAppResources/WebApp/static`` directory by running:

   .. code-block:: bash

     docker run --rm \
         -v=$PWD:/opt -w=/opt \
         "-u=$(id -u):$(id -g)"
         diracgrid/dirac-distribution:latest \
         /dirac-webapp-compile.py -D=/opt/src -n=DIRACWebAppResources --py3-style

2. Bump the version in ``setup.cfg`` and update the changelog in ``README.rst``.
3. Commit your changes, create a tag and push:

   .. code-block:: bash

     git add -p setup.cfg README.rst
     git commit -m "Update to $VERSION"
     git push --tags

4. Build the package for upload to PyPI:

   .. code-block:: bash

     python -m build

5. Upload the new release to PyPI:

   .. code-block:: bash

     twine upload dist/DIRACWebAppResources-VERSION*
