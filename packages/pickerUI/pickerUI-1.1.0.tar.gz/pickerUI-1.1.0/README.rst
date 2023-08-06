pickerUI
========

**pickerUI** is a small python library to help you create interactive selection list in the terminal. See it in action:


Installation
------------

::

    $ pip install pickerUI

Usage
-----

**pick** comes with a simple api::

    >>> from pickerUI import pick

    >>> target, level = pick({"A":[0,1,2], "B":[0,1,2]})
    >>> print(target, level)


**run**::

    python test.py

    A:
        0
     => 1
        2
    B:
        0
        1
        2


**output**::

    1 A
