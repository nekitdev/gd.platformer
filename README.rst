gd.platformer
=============

.. image:: https://img.shields.io/pypi/l/gd.platformer.svg
    :target: https://opensource.org/licenses/MIT
    :alt: Project License

.. image:: https://img.shields.io/pypi/v/gd.platformer.svg
    :target: https://pypi.python.org/pypi/gd.platformer
    :alt: PyPI Library Version

.. image:: https://img.shields.io/pypi/pyversions/gd.platformer.svg
    :target: https://pypi.python.org/pypi/gd.platformer
    :alt: Required Python Versions

.. image:: https://img.shields.io/pypi/status/gd.platformer.svg
    :target: https://github.com/nekitdev/gd.platformer/
    :alt: Project Development Status

.. image:: https://img.shields.io/pypi/dm/gd.platformer.svg
    :target: https://pypi.python.org/pypi/gd.platformer
    :alt: Library Downloads/Month

.. image:: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.herokuapp.com%2Fnekit%2Fpledges
    :target: https://patreon.com/nekit
    :alt: Patreon Page [Support]

gd.platformer is a library that implements Geometry Dash Platformer Mod in Python.

Installing
----------

**Python 3.6 or higher is required**

To install the library, you can just run the following command:

.. code:: sh

    # Windows
    py -3 -m pip install -U gd.platformer

In order to install the library from source, you can do the following:

.. code:: sh

    $ git clone https://github.com/nekitdev/gd.platformer
    $ cd gd.platformer
    $ python -m pip install -U .

Running
-------

Running the app is quite simple.

You can either invoke it from python:

.. code:: python3

    import gd.platformer

    gd.platformer.main()

Or run a console command:

.. code:: sh

    $ python -m gd.platformer

    # OR

    $ gd.platformer

Building
--------

You can build an executable file from the ``gd/platformer.py`` file using *PyInstaller*:

.. code:: sh

    $ pyinstaller --onefile --exclude-module PIL --exclude-module numpy --exclude-module IPython --exclude-module Crypto --exclude-module lxml --icon=icon.ico gd/platformer.py

Generated executable will be in ``./dist`` folder.

Authors
-------

This project is mainly developed by `nekitdev <https://github.com/nekitdev>`_ and `Sapfirenko <https://github.com/Sapphire1ne>`_.
Player rotation lock/unlock patch and dashing crash fix by `cos8o <https://github.com/Cos8o>`_.
