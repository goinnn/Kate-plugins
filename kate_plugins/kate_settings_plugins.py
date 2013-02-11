# -*- coding: utf-8 -*-
# Copyright (c) 2013 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import kate

from kate_core_plugins import move_menu_submenu, separated_menu

PY_MENU = "Python"
DJ_MENU = "Django"
PY_CHECKERS = "Checkers"
JS_MENU = "JavaScript"
TOOLS_MENU = "Tools"


@kate.init
def move_menus():
    py_menu_slug = PY_MENU.lower()
    dj_menu_slug = DJ_MENU.lower()
    py_checkers_slug = PY_CHECKERS.lower()
    separated_menu(py_menu_slug)
    move_menu_submenu(py_menu_slug, dj_menu_slug)
    separated_menu(py_menu_slug)
    move_menu_submenu(py_menu_slug, py_checkers_slug)


KATE_ACTIONS = {
    'insertIPDB': {'text': 'ipdb', 'shortcut': 'Ctrl+I',
                   'menu': PY_MENU, 'icon': None},
    'insertInit': {'text': '__init__', 'shortcut': 'Ctrl+-',
                   'menu': PY_MENU, 'icon': None},
    'insertSuper': {'text': 'super', 'shortcut': 'Alt+-',
                    'menu': PY_MENU, 'icon': None},
    'callRecursive': {'text': 'call recursive', 'shortcut': 'Ctrl+Alt+-',
                    'menu': PY_MENU, 'icon': None},
    'checkAll': {'text': 'Check all', 'shortcut': 'Alt+5',
                 'menu': PY_CHECKERS, 'icon': None},
    'checkPyflakes': {'text': 'pyflakes', 'shortcut': 'Alt+7',
                      'menu': PY_CHECKERS, 'icon': None},
    'parseCode': {'text': 'Parse code python', 'shortcut': 'Alt+6',
                  'menu': PY_CHECKERS, 'icon': None},
    'checkPep8': {'text': 'Pep8', 'shortcut': 'Alt+8',
                  'menu': PY_CHECKERS, 'icon': None},
    'createForm': {'text': 'Create Django Form', 'shortcut': 'Ctrl+Alt+F',
                   'menu': DJ_MENU, 'icon': None},
    'createModel': {'text': 'Create Django Model', 'shortcut': 'Ctrl+Alt+M',
                    'menu': DJ_MENU, 'icon': None},
    'importUrls': {'text': 'Template Django urls', 'shortcut': 'Ctrl+Alt+7',
                   'menu': DJ_MENU, 'icon': None},
    'importViews': {'text': 'Template import views', 'shortcut': 'Ctrl+Alt+v',
                    'menu': DJ_MENU, 'icon': None},
    'createBlock': {'text': 'Template block', 'shortcut': 'Ctrl+Alt+B',
                              'menu': DJ_MENU, 'icon': None},
    'closeTemplateTag': {'text': 'Close Template tag', 'shortcut': 'Ctrl+Alt+C',
                              'menu': DJ_MENU, 'icon': None},
    'insertReady': {'text': 'jQuery Ready', 'shortcut': 'Ctrl+J',
                    'menu': JS_MENU, 'icon': None},
    'checkJslint': {'text': 'JSLint', 'shortcut': 'Alt+9',
                    'menu': JS_MENU, 'icon': None},
    'togglePrettyJsonFormat': {'text': 'Pretty Json', 'shortcut': 'Ctrl+Alt+J',
                               'menu': JS_MENU, 'icon': None},
    'togglePrettyXMLFormat': {'text': 'Pretty XML', 'shortcut': 'Ctrl+Alt+X',
                              'menu': 'XML', 'icon': None},
}

PYTHON_AUTOCOMPLETE_ENABLED = True
JAVASCRIPT_AUTOCOMPLETE_ENABLED = True
JQUERY_AUTOCOMPLETE_ENABLED = True
CHECKALL_TO_SAVE = True
IGNORE_PEP8_ERRORS = []
TEMPLATE_TAGS_CLOSE = ["autoescape", "block", "comment", "filter", "for",
                       "ifchanged", "ifequal", "if", "spaceless", "with"]


try:
    from kate_settings_local import *
except ImportError:
    pass
