=======================
pysteps-importer-netcdf
=======================

Pysteps plugin adding importer for netcdf rain rate files generated within the PINCAST project (`radar_composite_generator` module).


License
=======
* MIT license


Documentation
=============

Currently provided importers:

* `importer_pincast_netcdf` - Importer for netcdf rain rate files generated within the PINCAST project (`radar_composite_generator` module).

Installation instructions
=========================

The latest development version of pysteps_importer_pincast can be installed using pip by running in a terminal:

    ::bash

    pip install git+https://github.com/ritvje/pysteps-importer-pincast.git

Test the plugin
===============

This plugin comes with a tester, which can also be used to test whether the plugin is correctly hooked up to pysteps.

Install pytest and run the tests with:

    ::bash

    pip install pytest
    pytest -v --tb=line


Credits
=======

- This package was created with Cookiecutter_ and the `pysteps/cookiecutter-pysteps-plugin`_ project template.


- The `pysteps/cookiecutter-pysteps-plugin`_ template was adapted from the cookiecutter-pypackage_
template.

.. _cookiecutter-pypackage: https://github.com/audreyfeldroy/cookiecutter-pypackage

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`pysteps/cookiecutter-pysteps-plugin`: https://github.com/pysteps/cookiecutter-pysteps-plugin
