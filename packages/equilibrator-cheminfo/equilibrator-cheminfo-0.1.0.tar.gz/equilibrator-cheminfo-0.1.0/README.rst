=============================
eQuilibrator Cheminformatics
=============================

.. image:: https://img.shields.io/pypi/v/equilibrator-cheminfo.svg
   :target: https://pypi.org/project/equilibrator-cheminfo/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/equilibrator-cheminfo.svg
   :target: https://pypi.org/project/equilibrator-cheminfo/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/equilibrator-cheminfo.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache Software License Version 2.0

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code Style Black

.. summary-start

Light adapter classes around Open Babel, RDKit, and ChemAxon for the functionality
needed in eQulibrator.

Install
=======

Please note that while ``equilibrator-cheminfo`` as a pure Python package is operating
system independent, the same is not true for the cheminformatics backends Open Babel, RDkit, or ChemAxon. While both
Open Babel and RDKit nowadays provide Python wheels, we do not test them on all
platforms.

RDKit
-----

.. code-block:: console

    pip install equilibrator-cheminfo[rdkit]

or

Open Babel
----------

.. code-block:: console

    pip install equilibrator-cheminfo[openbabel]

ChemAxon
--------

If you wish to use ChemAxon, you need to install the software, acquire a license, and
set the environment variable ``CHEMAXON_HOME``.

.. code-block:: console

    pip install equilibrator-cheminfo[chemaxon]

Copyright
=========

* Copyright © 2021, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0
  <https://www.apache.org/licenses/LICENSE-2.0>`_.

.. summary-end
