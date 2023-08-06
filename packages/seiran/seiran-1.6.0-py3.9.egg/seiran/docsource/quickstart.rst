Seiran Quickstart
=================

How to run
----------

Install Seiran by your preferred method. Most will probably want to run
``pip install seiran`` from the command line, but you can also install
from source with ``python setup.py install --user``. However or wherever
you do it, make sure Seiran's install location is on your system path,
so you can use Seiran anywhere just by typing “seiran [command]”.

Available commands:

.. code-block:: text

   seiran add [a bookmark]
   seiran del[ete a bookmark]
   seiran list [all bookmarks]
   seiran search [bookmarks]
   seiran edit [a bookmark]
   seiran import [bookmarks from various sources]
   seiran export [bookmarks to other formats]
   seiran clean [bookmarks]
   seiran copyright
   seiran help

Adding new bookmarks
--------------------

Use ``add`` to add a single new bookmark to the database. You’ll be
prompted for its title, URL, and optional “folder”/category. (The date
of creation will be added automatically.)

Optional arguments:

-t, --title
  A bookmark’s name. Usually appears in <h1> or <title> tags on the
  page.

-u, --url
  A bookmark’s Uniform Resource Locator. Must be unique.

-c, --category
  A bookmark’s category. This is inspired by Firefox’s folders, but you
  can put almost anything here.

Deleting bookmarks
------------------

You can remove a bookmark with the ``del`` command. Please be careful as
bookmarks cannot be recovered once they are deleted.

Optional arguments:

-u, --url
  The Universal Resource Locator of the bookmark you want to delete.

Editing bookmarks
-----------------

Use ``edit`` to modify an existing bookmark’s title or category/tag. To
avoid shenanigans, URLs cannot be edited in Seiran.

Optional arguments:

-u, --url
  The Universal Resource Locator of the bookmark you want to edit. Must
  be unique.

-f, --field
  The column you want to edit. Available arguments are ``title`` or
  ``category``.

-n, --new
  The new value you want an edited field to have.

Listing bookmarks
-----------------

You can see a list of all bookmarks with ``list``. This could take a
while for very large databases.

Finding bookmarks
-----------------

``search`` allows you to find a specific bookmark based on its title,
URL, date, or category.

-f, --field
  The column you want to search. Available arguments are ``title``,
  ``url``, ``category``, ``date``, or ``all``.

-q, --query
  The term you want to search for.

Exporting bookmarks
-------------------

With ``export``, you can export your bookmarks to a nicely-formatted,
timestamped file. Of course, you can easily get a plain CSV with a
simple SQLite command, so Seiran tries to add a bit of value by making
its output a bit prettier.

Available formats for exporting include HTML, TXT, and JSON.

Optional arguments:

-x, --exportformat
  The format you want to export your bookmarks to. Available arguments
  are ``txt``, ``html``, or ``json``.

Importing bookmarks
-------------------

Although it’s experimental, you can import a whole bunch of bookmarks at
once with the ``import`` command. Make sure to back up your existing
database before using, just in case.

When you use the ``import`` command, you’ll first be prompted to make
sure you *really* meant to do that – it could take a long time and add
quite a large number of bookmarks to your database (and may still have
bugs as well). If you’re OK with that, type ``y`` for yes. There is no
command-line argument to speed this along, just to make sure no
accidents happen.

Next, Seiran supports importation from existing Seiran databases,
Firefox (and derivatives, like IceCat), the
`OneTab <https://www.one-tab.com/>`__ browser add-on, and JSON exported
from Seiran itself (not arbitrary JSON files). You’ll be asked which one
you want to import bookmarks from.

Optional arguments:

-i, --importformat
  The system you want to import bookmarks from. Available arguments are
  ``firefox``, ``onetab``, ``seiran``, or ``json``.

Firefox et al.
~~~~~~~~~~~~~~

If you exported a bookmarks backup file from Firefox 3.0 onwards, and
it’s not an HTML document you can view in your browser, it’s probably a
JSON file. Just enter the path to that file the importation process will
begin:

.. code-block:: text

    $ seiran import -i firefox
    seiran by gargargarrick, v.1.6.0.
    Are you sure you want to import bookmarks? It might take a while. Back up your database first! (y/n) > y
    Please enter the path to the Firefox profile directory OR the Firefox bookmarks JSON file from which you wish to import. > bookmarks-2021-02-20.json
    Preparing Firefox JSON bookmarks...
    283 bookmarks loaded from bookmarks-2021-02-20.json.
    [...]

You can also import bookmarks directly from Firefox’s browser profile
directory, if you want. You’ll have to tell Seiran directly where it is;
this varies enough that it can’t be determined automatically.

PC browsers
^^^^^^^^^^^

In the browser that you want to import from, either select
``Help > Troubleshooting information`` from the main menu or simply
navigate to ``about:support``. Scroll down to “Profile Folder” and press
the “Show Folder” button. The profile folder will open up in your file
manager; copy its path and paste that into Seiran’s prompt.

Seiran will ask if this is a mobile browser’s profile; say no, and the
importation process will begin.

Android browsers
^^^^^^^^^^^^^^^^

If you have access to an Android browser’s profile (because you copied
it with an add-on like `Copy
Profile <https://addons.mozilla.org/en-US/android/addon/copy-profile/>`__
and ADB, or are running Seiran itself on a rooted mobile device through
science or magic), just point Seiran to the directory that contains
``browser.db`` (not the file itself).

Seiran will ask if this is a mobile browser’s profile; say yes, and the
importation process will begin.

OneTab
~~~~~~

Save the contents of OneTab’s “Export URLs” into a plain text (.txt)
file. When prompted by Seiran, copy and paste the path to the export
file. Then the importation process will begin.

Caveat: OneTab does not store dates in its export file, so those will
not be preserved by Seiran. The date that you imported the bookmark will
be used instead.

Of course, the file does not literally need to have been exported by
OneTab. You can also use this mode to import arbitrary plain-text lists
of bookmarks, as long as each follows the format ``URL | Title``.

.. _seiran-1:

Seiran
~~~~~~

If you have another Seiran database and you want to combine it with your
main one, this function will allow that. It is highly experimental and
may ruin all the things. I am not responsible if you lose your
bookmarks; make sure both databases are backed up before you attempt
this.

Seiran will prompt you for the **full path** to the database you want to
import. Provide it and the importation process will begin.

Cleaning bookmarks
------------------

``seiran clean`` will look for bookmarks in your database that don’t
seem to have titles, and add their respective URL as a title instead. It
will then look for bookmarks that have identical titles (which suggests
they might be duplicates) and tell you if it finds any.

License
-------

Copyright 2015-2021 Matthew Ellison.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, see http://www.gnu.org/licenses or write to:

   | Free Software Foundation
   | 51 Franklin Street, Fifth Floor
   | Boston, MA 02110-1335
   | USA
