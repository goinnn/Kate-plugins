KATE_ACTIONS = {
    'insertIPDB': {'text': 'ipdb', 'shortcut': 'Ctrl+I',
                   'menu': 'Edit', 'icon': None},
    'insertInit': {'text': '__init__', 'shortcut': 'Ctrl+-',
                   'menu': 'Edit', 'icon': None},
    'insertSuper': {'text': 'super', 'shortcut': 'Alt+-',
                    'menu': 'Edit', 'icon': None},
    'callRecursive': {'text': 'call recursive', 'shortcut': 'Ctrl+Alt+-',
                    'menu': 'Edit', 'icon': None},
    'checkAll': {'text': 'Check all', 'shortcut': 'Alt+5',
                 'menu': 'Edit', 'icon': None},
    'checkPyflakes': {'text': 'pyflakes', 'shortcut': 'Alt+7',
                      'menu': 'Edit', 'icon': None},
    'parseCode': {'text': 'Parse code python', 'shortcut': 'Alt+6',
                  'menu': 'Edit', 'icon': None},
    'checkPep8': {'text': 'Pep8', 'shortcut': 'Alt+8',
                  'menu': 'Edit', 'icon': None},
    'createForm': {'text': 'Create Django Form', 'shortcut': 'Ctrl+Alt+F',
                   'menu': 'Edit', 'icon': None},
    'createModel': {'text': 'Create Django Model', 'shortcut': 'Ctrl+Alt+M',
                    'menu': 'Edit', 'icon': None},
    'importUrls': {'text': 'Template Django urls', 'shortcut': 'Ctrl+Alt+7',
                   'menu': 'Edit', 'icon': None},
    'importViews': {'text': 'Template import views', 'shortcut': 'Ctrl+Alt+v',
                    'menu': 'Edit', 'icon': None},
    'insertReady': {'text': 'jQuery Ready', 'shortcut': 'Ctrl+J',
                    'menu': 'Edit', 'icon': None},
    'checkJslint': {'text': 'JSLint', 'shortcut': 'Alt+J',
                    'menu': 'Edit', 'icon': None},
    'togglePrettyJsonFormat': {'text': 'Pretty Json', 'shortcut': 'Ctrl+Alt+J',
                               'menu': 'Edit', 'icon': None},
    'togglePrettyXMLFormat': {'text': 'Pretty XML', 'shortcut': 'Ctrl+Alt+X',
                              'menu': 'Edit', 'icon': None},
}

PYTHON_AUTOCOMPLETE_ENABLED = True
JAVASCRIPT_AUTOCOMPLETE_ENABLED = True
JQUERY_AUTOCOMPLETE_ENABLED = True
CHECKALL_TO_SAVE = True
IGNORE_PEP8_ERRORS = []

try:
    from kate_settings_local import *
except ImportError:
    pass
