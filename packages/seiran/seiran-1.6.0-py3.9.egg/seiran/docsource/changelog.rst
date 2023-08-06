Seiran Changelog
====================

1.6.0
-----

-  Cleaned up code basically everywhere.
-  Added JSON import and export.

1.5.1
-----

-  Fixed bug in ``seiran del``.

1.5.0
-----

-  ``seiran list`` and ``seiran search`` output now includes a
   Markdown-like title heading.
-  Made ``seiran edit`` output more clear.
-  Updated copyright year.
-  Updated docstrings.
-  Minor cleanup.

1.4.0
-----

-  Removing references to GitHub in protest of their contract with ICE.
-  ``date`` is now a searchable field for ``seiran search``.

1.3.3
-----

-  ``seiran edit`` now displays the active bookmark’s information
   properly (like other commands do)

1.3.2
-----

-  Fixed wrong filename for readme in ``setup.py``
-  Added some trailing spaces to ``seiran search`` output output so you
   can pipe it to a file and parse it as Markdown, and thus generate
   HTML from it (some commands already had this feature; I’d just
   forgotten it for search)

1.3.1
-----

-  Fixed a bug where ``seiran del`` no longer worked correctly

1.3.0
-----

-  ``seiran clean`` now checks if any bookmarks have identical titles.
-  Changelog created.

1.2.0
-----

-  Command line functionality has been improved. You may now pass
   arguments to Seiran commands.
-  A new command, ``seiran clean``, checks if any bookmarks have empty
   titles.

1.1
---

-  Adding a new importer for other Seiran databases.

1.0
---

Initial release.