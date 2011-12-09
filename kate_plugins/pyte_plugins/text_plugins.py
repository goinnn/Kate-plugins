import kate
import re

from utils import insertText

TEXT_INIT =  """
    def __init__(self, *args, **kwargs):
        super(%s, self).__init__(*args, **kwargs)
"""

TEXT_SUPER =  """%ssuper(%s, %s).%s(%s)"""

patter_blank = "(?:\ |\t|\n)*"
patter_espaces = "([\ |\t|\n]*)"
pattern_class = re.compile("class %s(\w+)\(([\w|.]+)\):" % patter_blank)

patter_params = "([\w|\,|\ |\t|\n|\'|\"|\.|\=]*)"
def_init = "%(espaces)sdef %(blank)s(\w+)%(blank)s\(%(param)s" % {"blank": patter_blank,
                                                         "espaces": patter_espaces,
                                                         "param": patter_params}
def_finish = "(?:.*)\):"
pattern_def_init = re.compile(def_init, re.MULTILINE|re.DOTALL)
pattern_def_finish = re.compile(def_finish, re.MULTILINE|re.DOTALL)
pattern_def = re.compile("%s\):" % def_init, re.MULTILINE|re.DOTALL)

pattern_param = re.compile("(\w+)%(blank)s=%(blank)s(.*)" % {"blank": patter_blank})



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
        currentLine = currentLine -1
    insertText(TEXT_INIT % class_name)


def change_kwargs(param):
    match = pattern_param.match(param)
    if match:
        return '%s=%s' % (match.groups()[0], match.groups()[0])
    return param


@kate.action('super', shortcut='Alt+-', menu='Edit')
def insertSuper():
    class_name = 'XXX'
    function_name = 'XXX'
    params = ['self', '*args', '**kwargs']
    espaces = ' ' * 4
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    currentLine = currentPosition.line()
    find_finish_def = False
    while currentLine >= 0:
        text = unicode(currentDocument.line(currentLine))
        if find_finish_def:                        
            text_def = '%s\n%s' %(text, text_def)
        else:
            text_def = text
        if function_name == 'XXX':
            match_finish = pattern_def_finish.match(text_def)
            match_init = pattern_def_init.match(text_def)
            if match_finish and match_init:
                match = pattern_def.match(text_def)
                espaces = match.groups()[0] + ' ' * 4
                function_name = match.groups()[1]
                params = match.groups()[2].split(',')
                params = [change_kwargs(param.strip(' \t')) for param in params]
            elif match_finish:
                find_finish_def = True
        match = pattern_class.match(text)
        if match:
            class_name = match.groups()[0]
            break
        currentLine = currentLine -1
    text = unicode(currentDocument.line(currentPosition.line())).strip()
    text_super_template = TEXT_SUPER
    if not text:
        text_super_template = text_super_template + '\n'
        currentDocument.removeLine(currentPosition.line())
    else:
        espaces = ''
    insertText(text_super_template % (espaces, class_name, params[0], function_name, ', '.join(params[1:])))

