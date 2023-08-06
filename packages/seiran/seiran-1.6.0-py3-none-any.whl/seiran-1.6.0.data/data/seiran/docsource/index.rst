.. Seiran documentation master file, created by
   sphinx-quickstart on Tue Jun 29 01:59:38 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Seiran Documentation
====================

Seiran (/'seIran/, lit. blue-indigo) is a simple bookmarks manager. It's free software and cross-platform, built with Python and SQLite.

Seiran stores *your* bookmarks on *your* machine, where they belong. It's ideal if you

+ are tired of slowing down your browser with huge bookmark files
+ have bookmarks you don't trust others with
+ reject proprietary, black-box "cloud" services on principle
+ want to back up your bookmarks regularly, in a format that will work with any browser, just in case
+ use multiple different browsers or browser profiles
+ want to be able to edit your bookmarks with familiar SQL tools instead of a slow in-browser PHP interface
+ prefer terminals over GUI

Or all of the above!

Seiran does not connect to the Internet at any time. It does not download icons or validate your bookmarks. It does not automatically synchronize with anything. It doesn't even have an "open in browser" command. It may not be *that* useful, and it's certainly nothing fancy, but it does exactly what I want and need a bookmark manager to do.

At present Seiran is text-only. I've considered making a GUI interface for it, but the command line one works fine for now.

Dependencies
------------

+ Python >= 3.4
+ appdirs

That's all!

--------------

.. toctree::
   :maxdepth: 4
   :caption: Contents:
   
   modules
   quickstart
   changelog



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
