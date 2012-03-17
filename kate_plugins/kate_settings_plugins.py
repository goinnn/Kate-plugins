import kate

from PyKDE4 import kdeui
from PyQt4 import QtGui

KATE_ACTIONS = {
    'insertIPDB': {'text': 'ipdb', 'shortcut': 'Ctrl+I',
                   'menu': 'python-templates', 'icon': None},
    'insertInit': {'text': '__init__', 'shortcut': 'Ctrl+-',
                   'menu': 'python-templates', 'icon': None},
    'insertSuper': {'text': 'super', 'shortcut': 'Alt+-',
                    'menu': 'python-templates', 'icon': None},
    'callRecursive': {'text': 'call recursive', 'shortcut': 'Ctrl+Alt+-',
                    'menu': 'python-templates', 'icon': None},
    'checkAll': {'text': 'Check all', 'shortcut': 'Alt+5',
                 'menu': 'checkers', 'icon': None},
    'checkPyflakes': {'text': 'pyflakes', 'shortcut': 'Alt+7',
                      'menu': 'checkers', 'icon': None},
    'parseCode': {'text': 'Parse code python', 'shortcut': 'Alt+6',
                  'menu': 'checkers', 'icon': None},
    'checkPep8': {'text': 'Pep8', 'shortcut': 'Alt+8',
                  'menu': 'checkers', 'icon': None},
    'createForm': {'text': 'Create Django Form', 'shortcut': 'Ctrl+Alt+F',
                   'menu': 'django-templates', 'icon': None},
    'createModel': {'text': 'Create Django Model', 'shortcut': 'Ctrl+Alt+M',
                    'menu': 'django-templates', 'icon': None},
    'importUrls': {'text': 'Template Django urls', 'shortcut': 'Ctrl+Alt+7',
                   'menu': 'django-templates', 'icon': None},
    'importViews': {'text': 'Template import views', 'shortcut': 'Ctrl+Alt+v',
                    'menu': 'django-templates', 'icon': None},
    'insertReady': {'text': 'jQuery Ready', 'shortcut': 'Ctrl+J',
                    'menu': 'js-templates', 'icon': None},
    'checkJslint': {'text': 'JSLint', 'shortcut': 'Alt+J',
                    'menu': 'checkers', 'icon': None},
    'togglePrettyJsonFormat': {'text': 'Pretty Json', 'shortcut': 'Ctrl+Alt+J',
                               'menu': 'pretty-print', 'icon': None},
    'togglePrettyXMLFormat': {'text': 'Pretty XML', 'shortcut': 'Ctrl+Alt+X',
                              'menu': 'pretty-print', 'icon': None},
}

PYTHON_AUTOCOMPLETE_ENABLED = True
JAVASCRIPT_AUTOCOMPLETE_ENABLED = True
JQUERY_AUTOCOMPLETE_ENABLED = True
CHECKALL_TO_SAVE = True
IGNORE_PEP8_ERRORS = []


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
create_menu('Checkers', 'checkers', 'tools')
create_menu('Pretty print', 'pretty-print', 'tools')


try:
    from kate_settings_local import *
except ImportError:
    pass
