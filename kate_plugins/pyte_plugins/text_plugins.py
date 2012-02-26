import kate
import re

from utils import insertText

TEXT_INIT = """
    def __init__(self, *args, **kwargs):
        super(%s, self).__init__(*args, **kwargs)
"""

TEXT_SUPER = """%ssuper(%s, %s).%s(%s)"""

str_blank = "(?:\ |\t|\n)*"
str_espaces = "([\ |\t|\n]*)"
pattern_espaces = re.compile("%s(.*)" % str_espaces)
pattern_class = re.compile("%(str_blank)sclass %(str_blank)s(\w+)\(([\w|., ]+)\):" % {'str_blank': str_blank})

str_params = "(.*)"
str_def_init = "%(espaces)sdef %(blank)s(\w+)%(blank)s\(%(param)s" % {
                                                "blank": str_blank,
                                                "espaces": str_espaces,
                                                "param": str_params}
str_def_finish = "(?:.*)\):"
pattern_def_init = re.compile(str_def_init, re.MULTILINE | re.DOTALL)
pattern_def_finish = re.compile(str_def_finish, re.MULTILINE | re.DOTALL)
pattern_def = re.compile("%s\):" % str_def_init, re.MULTILINE | re.DOTALL)

pattern_param = re.compile("%(espaces)s(\w+)%(blank)s\=%(blank)s(.*)" % {
                                                "blank": str_blank,
                                                "espaces": str_espaces},
                                                re.MULTILINE | re.DOTALL)

PYTHON_SPACES = 4


@kate.action('ipdb', shortcut='Ctrl+I', menu='Edit')
def insertIPDB():
    insertText("import ipdb; ipdb.set_trace()")


@kate.action('__init__', shortcut='Ctrl+-', menu='Edit')
def insertInit():
    class_name = 'XXX'
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    currentLine = currentPosition.line()
    while currentLine >= 0:
        text = unicode(currentDocument.line(currentLine))
        match = pattern_class.match(text)
        if match:
            class_name = match.groups()[0]
            break
        currentLine = currentLine - 1
    insertText(TEXT_INIT % class_name)


def change_kwargs(param):
    match = pattern_param.match(param)
    if match:
        return '%s%s=%s' % (match.groups()[0],
                            match.groups()[1],
                            match.groups()[1])
    return param


def get_number_espaces(currentDocument, currentLine,
                       parentheses=0, initial_instruct=False):
    line_before = unicode(currentDocument.line(currentLine - 1))
    if not line_before.strip() and currentLine >= 0:
        return get_number_espaces(currentDocument, currentLine - 1,
                                  parentheses=parentheses,
                                  initial_instruct=initial_instruct)
    match = pattern_espaces.match(line_before)
    if match:
        if line_before.endswith(":") or parentheses > 0 or initial_instruct:
            parentheses += line_before.count(")") - line_before.count("(")
            line_before = line_before.strip()
            if parentheses == 0 and (line_before.startswith("for") or
                                     line_before.startswith("if") or
                                     line_before.startswith("while") or
                                     line_before.startswith("def")):
                return PYTHON_SPACES + len(match.groups()[0])
            return get_number_espaces(currentDocument, currentLine - 1,
                                      parentheses=parentheses,
                                      initial_instruct=True)
        return len(match.groups()[0])
    return PYTHON_SPACES * 2


@kate.action('super', shortcut='Alt+-', menu='Edit')
def insertSuper():
    class_name = 'XXX'
    function_name = 'XXX'
    params = ['self', '*args', '**kwargs']
    espaces = ' ' * PYTHON_SPACES
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    currentLine = currentPosition.line()
    find_finish_def = False
    number_espaces = PYTHON_SPACES * 2
    parentheses = 0
    text_def = ''
    while currentLine >= 0:
        text = unicode(currentDocument.line(currentLine))
        if find_finish_def:
            text_def = '%s\n%s' % (text, text_def)
        else:
            text_def = text
        if function_name == 'XXX':
            match_finish = pattern_def_finish.match(text_def)
            match_init = pattern_def_init.match(text_def)
            if match_finish and match_init:
                match = pattern_def.match(text_def)
                number_espaces = get_number_espaces(currentDocument,
                                                    currentPosition.line())
                if not number_espaces:
                    number_espaces = len(match.groups()[0]) + 1
                espaces = ' ' * number_espaces
                function_name = match.groups()[1]
                params = match.groups()[2].split(',')
                params = [change_kwargs(param.strip(' \t'))
                            for param in params]
            elif match_finish:
                find_finish_def = True
                parentheses += text_def.count(")") - text_def.count("(")
            if find_finish_def and parentheses <= 0:
                parentheses += text_def.count(")") - text_def.count("(")
                find_finish_def = False
        match = pattern_class.match(text)
        if match:
            class_name = match.groups()[0]
            break
        currentLine = currentLine - 1
    text = unicode(currentDocument.line(currentPosition.line())).strip()
    text_super_template = TEXT_SUPER
    if not text:
        text_super_template = text_super_template + '\n'
        currentDocument.removeLine(currentPosition.line())
    else:
        espaces = ''
    insertText(text_super_template % (espaces, class_name, params[0],
                                      function_name, ', '.join(params[1:])))
