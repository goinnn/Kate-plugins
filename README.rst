.. contents::

============
Kate Plugins
============

Information
===========

These are plugins to `Kate <http://kate-editor.org  />`_ editor. Plugins to make coding easier in `Python <http://python.org/>`_, `Django <https://docs.djangoproject.com>`_ and JavaScript

Requeriments
============

 * `Pâté <http://paul.giannaros.org/pate/>`_

Installation
============

 * `Install Pâté <https://github.com/pag/pate/blob/master/INSTALL.txt>`_
 * `Install Pysmell <http://pypi.python.org/pypi/pysmell>`_ (easy_install pysmell)
 * Install the plugins:

::

 easy_install Kate-plugins
 cd ~/.kde/share/apps/kate/pate/
 ln -s /PATH/OF/THE/EGG/kate_plugins/ .


or

::

 cd ~/
 git clone git://github.com/goinnn/Kate-plugins.git
 cd ~/.kde/share/apps/kate/pate/
 ln -s ~/Kate-plugins/kate_plugins/ .

Plugins
=======

Autocomplete to python (python)
-------------------------------

 * Shortcut: It is automatical
 * from and import instruction (beta)
 * autocomplete into the code (alpha) with `pysmell <http://pypi.python.org/pypi/pysmell>`_
 * There was a hook if you want to add your own packages python in the autocomplete structure. You should be create a file called "autocomplete_path.py" next to the "autocomplete.py" with a function "def path(doc, view)", like this:
 * **Currently working on this plugin**

::

 def path(doc, view):
     return ['/PATH/OF/THE/EGG1/name1.egg',
             '/PATH/OF/THE/EGG2/name2.egg',
             ...
             '/PATH/OF/THE/EGGN/namen.egg'] 

insert IPDB (python)
--------------------

 * Shortcut: Ctrl+I
 * Insert the text "import ipdb; ipdb.set_trace()"


insert __init__ (python)
------------------------

 * Shortcut: Ctrl+-
 * Smart insert a function __init__

insert super (python)
------------------------

 * Shortcut: Alt+-
 * Smart insert a call to super of the function


template urls (django)
----------------------
 * Shortcut: Ctrl+Alt+7
 * Smart template of the file `urls.py <http://docs.djangoproject.com/en/dev/topics/http/urls/#example>`_


import views (django)
----------------------
 * Shortcut: Ctrl+Alt+v
 * Insert the tipical imports in a view


Create form (django)
----------------------
 * Shortcut: Ctrl+Alt+F
 * Template to form class


Create model (django)
----------------------
 * Shortcut: Ctrl+Alt+M
 * Template to model class


jQuery ready (js)
-----------------
 * Shortcut: Ctrl+J
 * Template jQuery ready

Pretty JSON (js)
----------------
 * Shortcut: Ctrl+Alt+J
 * Convert a horrible json in a pretty JSON :-)


Future Plugins
==============

 * Call recursive
 * `pep8 <http://www.python.org/dev/peps/pep-0008/>`_
 * `pyflakes <http://pypi.python.org/pypi/pyflakes>`_
 * `jslint <http://www.jslint.com/>`_

Other repositories of Plugins to Kate
=====================================

 * http://github.com/mtorromeo/kate-plugin-zencoding (Very recomended)
 * https://github.com/pag/pate/tree/master/src/plugins
 * https://github.com/emyller/pate-plugins
 * http://code.google.com/p/kate-pate-plugins/
