# -*- coding: utf-8 -*-
# Copyright (c) 2011 by Pablo Martín <goinnn@gmail.com>
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

from kate_core_plugins import create_mainmenu, create_submenu, separated_menu

PY_MENU = create_mainmenu('Python', 'python')
DJ_MENU = create_submenu('Django', 'django', PY_MENU)
separated_menu(PY_MENU)
PY_CHECKERS = create_submenu('Checkers', 'py_checkers', PY_MENU)

JS_MENU = create_mainmenu('Javascript', 'javascript')
JS_CHECKERS = create_submenu('Checkers', 'js_checkers', JS_MENU)
separated_menu(JS_MENU)

TOOLS_MENU = 'tools'
separated_menu(TOOLS_MENU)
PR_MENU = create_submenu('Pretty print', 'pretty-print', TOOLS_MENU)
separated_menu(TOOLS_MENU)


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
    'checkJslint': {'text': 'JSLint', 'shortcut': 'Alt+J',
                    'menu': JS_CHECKERS, 'icon': None},
    'togglePrettyJsonFormat': {'text': 'Pretty Json', 'shortcut': 'Ctrl+Alt+J',
                               'menu': PR_MENU, 'icon': None},
    'togglePrettyXMLFormat': {'text': 'Pretty XML', 'shortcut': 'Ctrl+Alt+X',
                              'menu': PR_MENU, 'icon': None},
}

PYTHON_AUTOCOMPLETE_ENABLED = True
JAVASCRIPT_AUTOCOMPLETE_ENABLED = True
JQUERY_AUTOCOMPLETE_ENABLED = True
CHECKALL_TO_SAVE = True
IGNORE_PEP8_ERRORS = []
TEMPLATE_TAGS_CLOSE = ["autoescape", "block", "comment", "filter", "for", "if",
                       "ifchanged", "ifequal", "spaceless", "with"]


try:
    from kate_settings_local import *
except ImportError:
    pass
