import kate
import re

from utils import insertText

TEXT_INIT =  """
    def __init__(self, *args, **kwargs):
        super(%s, self).__init__(*args, **kwargs)
"""

TEXT_SUPER =  """%ssuper(%s, %s).%s(%s)"""

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
    pattern = re.compile("class (.*)\((.*)\):")
    while currentLine >= 0:
        text = unicode(currentDocument.line(currentLine))
        match = pattern.match(text)
        if match:
            class_name = match.groups()[0]
            break
        currentLine = currentLine -1
    insertText(TEXT_INIT % class_name)


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
    pattern_class = re.compile("class (.*)\((.*)\):")
    pattern_def = re.compile("( *)def (.*)\((.*)\):")
    while currentLine >= 0:
        text = unicode(currentDocument.line(currentLine))
        if function_name == 'XXX':
            match = pattern_def.match(text)
            if match:
                espaces = match.groups()[0] + ' ' * 4
                function_name = match.groups()[1]
                params = match.groups()[2].split(',')
                params = [param.strip() for param in params]
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

