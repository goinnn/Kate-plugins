import compiler

import kate

from PyQt4 import QtCore

from utils import is_mymetype_python
from pyte_plugins.check_plugins.commons import showOk, showErrors, canCheckDocument


@kate.action('parse code', shortcut='Alt+6', menu='Edit')
def parseCode(doc=None):
    if not canCheckDocument(doc, text_plain=True):
        return
    doc = doc or kate.activeDocument()
    text = unicode(doc.text())
    try:
        code = compiler.parse(text)
        showOk('Parse code Ok')
    except SyntaxError, e:
        error = {}
        error['filename'] = e.filename
        error['text'] = e.text
        error['line'] = e.lineno
        showErrors([error])


def createSignalCheckDocument(view, *args, **kwargs):
    doc = view.document()
    doc.modifiedChanged.connect(parseCode)

windowInterface = kate.application.activeMainWindow()
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalCheckDocument)
