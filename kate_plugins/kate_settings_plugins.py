from kate_core_plugins import create_submenu, separated_menu

separated_menu('edit')
DJ_MENU = create_submenu('Django Templates', 'django-templates', 'edit')
PY_MENU = create_submenu('Python Templates', 'python-templates', 'edit')
JS_MENU = create_submenu('Js Templates', 'js-templates', 'edit')
separated_menu('edit')
separated_menu('tools')
CH_MENU = create_submenu('Checkers', 'checkers', 'tools')
PR_MENU = create_submenu('Pretty print', 'pretty-print', 'tools')
separated_menu('tools')

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
                 'menu': CH_MENU, 'icon': None},
    'checkPyflakes': {'text': 'pyflakes', 'shortcut': 'Alt+7',
                      'menu': CH_MENU, 'icon': None},
    'parseCode': {'text': 'Parse code python', 'shortcut': 'Alt+6',
                  'menu': CH_MENU, 'icon': None},
    'checkPep8': {'text': 'Pep8', 'shortcut': 'Alt+8',
                  'menu': CH_MENU, 'icon': None},
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
                    'menu': CH_MENU, 'icon': None},
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
