import kate

from utils import insertText

TEXT_INIT =  """
    def __init__(self, *args, **kwargs):
        super(%s, self).__init__(*args, **kwargs)
"""


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