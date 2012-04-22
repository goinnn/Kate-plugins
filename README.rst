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
* Extra dependencies for extra and super nice features. Optional, but **very recomended** :)

    * Install `Pysmell <http://pypi.python.org/pypi/pysmell>`_
    * Install `PEP8 <http://pypi.python.org/pypi/pep8>`_
    * Install `PyFlakes <http://pypi.python.org/pypi/pyflakes>`_
    * Install `pyjslint <http://pypi.python.org/pypi/pyjslint>`_ (it requires `NodeJS <http://nodejs.org/>`_, read the pyjslint readme)

::

 easy_install pysmell==0.7.3
 easy_install pep8==0.6.1
 easy_install pyflakes==0.5.0
 easy_install pyjslint==0.3.3

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

Autocomplete (python)
---------------------

 * Shortcut: It is automatical
 * from and import instruction
 * autocomplete into the code (beta) with `pysmell <http://pypi.python.org/pypi/pysmell>`_
 * There was a hook if you want to add your own packages python in the autocomplete structure. You should be create a file called "autocomplete_path.py" next to the "autocomplete.py" with a function "def path(session, doc, view)", like this:

::

 def path(session, doc, view):
     if session == 'session1'
        return ['/PATH/OF/THE/EGG1/name1.egg',
                '/PATH/OF/THE/PACKAGE1/',
                ...
                '/PATH/OF/THE/EGGN/namen.egg'] 
     elif session == 'session2':
        return ['/PATH/OF/THE/EGG2/name2.egg',
                '/PATH/OF/THE/PACKAGE2/',
                ...
                '/PATH/OF/THE/EGGN/namem.egg'] 
      else:
        return ['/PATH/OF/THE/EGG2/name3.egg',
                '/PATH/OF/THE/PACKAGE3/',
                ...
                '/PATH/OF/THE/EGGN/namel.egg'] 


insert IPDB (python)
--------------------

 * Shortcut: Ctrl+I
 * Insert the text "import ipdb; ipdb.set_trace()"


insert __init__ (python)
------------------------

 * Shortcut: Ctrl+-
 * Smart insert a function __init__

insert super (python)
---------------------

 * Shortcut: Alt+-
 * Smart insert a call to super of the function

insert call recursive (python)
------------------------------

 * Shortcut: Ctrl+Alt+-
 * Smart insert a call to the current function recursively

PEP8 (python)
-------------
 * Shortcut: Alt+8
 * Use PEP8 to look for ugly code, highlights lines with problems
 * It uses `pep8 <http://pypi.python.org/pypi/pep8>`_ so it must be present in the system

PyFlakes (python)
-----------------
 * Shortcut: Alt+7
 * Use PyFlakes to look for bad code, highlights lines with problems
 * It uses `pyflakes <http://pypi.python.org/pypi/pyflakes>`_ so it must be present in the system

Parse syntax (python)
---------------------

 * Shortcut: Alt+6 or when you save the file
 * Parse syntax this file and show a error list, or a dialog say "OK"

Check All (python/javascript)
-----------------------------

 * Shortcut: Alt+5
 * Check pep8, pyflakes, parse syntax and jslint

Template Django urls (django)
-----------------------------
 * Shortcut: Ctrl+Alt+7
 * Smart template of the file `urls.py <http://docs.djangoproject.com/en/dev/topics/http/urls/#example>`_


Template import views (django)
------------------------------
 * Shortcut: Ctrl+Alt+V
 * Insert the tipical imports in a view


Create Django form (django)
---------------------------
 * Shortcut: Ctrl+Alt+F
 * Template to form class


Create Django model (django)
----------------------------
 * Shortcut: Ctrl+Alt+M
 * Template to model class


Close Template tag (django)
----------------------------
 * Shortcut: Ctrl+Alt+C
 * Close the last open templatetag (block, if, for, etc)

Template block (django)
----------------------------
 * Shortcut: Ctrl+Alt+B
 * Insert a struncture like this: {% block content %}XXX{% endblock %} or {% if x > 3 %} {% endif %}

Autocomplete static to javascript (javascript)
----------------------------------------------
 * Shortcut: It is automatical

Autocomplete static to jQuery (javascript)
----------------------------------------------
 * Shortcut: It is automatical

jQuery ready (javascript)
-------------------------
 * Shortcut: Ctrl+J
 * Template jQuery ready

Pretty JSON (javascript)
------------------------
 * Shortcut: Ctrl+Alt+J
 * Convert a horrible json in a pretty JSON :-)

JSLint (javascript)
-------------------
 * Shortcut: Alt+J
 * Use JSLint to look for errors and bad code, highlights lines with problems
 * It uses `pyjslint <http://pypi.python.org/pypi/pyjslint>`_ so it must be present in the system (and working!)

Pretty XML (xhtml)
------------------------
 * Shortcut: Ctrl+Alt+X
 * Convert a horrible xml in a pretty XML :-)

Future Plugins
==============

 * Clean code (core)
 * Improve autocompletes plugins (core)
 * Template tags autocomplete (django)
 * Integration with rope (python)

Other repositories of Plugins to Kate
=====================================

 * http://github.com/mtorromeo/kate-plugin-zencoding (Very recomended)
 * https://github.com/pag/pate/tree/master/src/plugins
 * https://github.com/emyller/pate-plugins
 * http://code.google.com/p/kate-pate-plugins/
