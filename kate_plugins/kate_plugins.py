from PyKDE4 import kdeui
from PyQt4 import QtGui

from jste_plugins.autocomplete import *
from jste_plugins.jquery_plugins import *
from jste_plugins.json_plugins import *
try:
    from jste_plugins.jslint_plugins import *
except ImportError:
    pass
try:
    from pyte_plugins.autocomplete.autocomplete import *
except ImportError:
    pass

from pyte_plugins.djte_plugins.class_plugins import *
from pyte_plugins.djte_plugins.text_plugins import *
from pyte_plugins.text_plugins import *
from pyte_plugins.check_plugins.parse_plugins import *

try:
    from pyte_plugins.check_plugins.cheack_all_plugins import *
except ImportError:
    pass
try:
    from pyte_plugins.check_plugins.pep8_plugins import *
except ImportError:
    pass

try:
    from pyte_plugins.check_plugins.pyflakes_plugins import *
except ImportError:
    pass

from xhtml_plugins.xml_plugins import *


def create_menu(name_menu, slug_menu, menu_parent_slug):
    windowInterface = kate.application.activeMainWindow()
    window = windowInterface.window()
    menu_parent = None

    for menu in window.findChildren(QtGui.QMenu):
        if str(menu.objectName()) == menu_parent_slug:
            menu_parent = menu
            break
    if not menu_parent:
        return
    new_menu = kdeui.KMenu(name_menu, window)
    new_menu.setObjectName(slug_menu)

    action = QtGui.QAction(name_menu, new_menu)
    action.setObjectName(slug_menu)
    action.setMenu(new_menu)
    menu_parent.addAction(action)


create_menu('Django Templates', 'django-templates', 'edit')
create_menu('Python Templates', 'python-templates', 'edit')
create_menu('Js Templates', 'js-templates', 'edit')
create_menu('Checkers', 'checkers', 'edit')
create_menu('Utils', 'utils', 'edit')
