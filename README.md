# Python Duplicates

> `Python Duplicates` script can be use to find duplicates in filesystem, and
> able you to take various action on them.

Usage
-----

```
usage: py_duplicates.py [-h] [-d] [-i] path

Python Duplicates - Find duplicate

positional arguments:
  path               path where to find duplicates

optional arguments:
  -h, --help         show this help message and exit
  -d, --delete       delete all files with duplicates
  -i, --interactive  interactively manage duplicates
```

TODO
----

`Python Duplicates` is a work in progress, so any ideas and patches are appreciated.

* [x] Find duplicates
* [ ] Take action
    * Interactive actions
        * [x] Open in text editor
    * [x] Delete All duplicates
    * [x] Move to another directory
* [ ] Improve output display
* [ ] Additional useful information on summary
    * [ ] Like percentage of path consumed by duplicates

Contributing
------------

Feel free to improve `Python Duplicates`. All kind of pull-requests are welcome.

LICENSE
------

`Python Duplicates` is licensed under
[GPL3](https://github.com/nagracks/py_duplicates/blob/master/LICENSE)
