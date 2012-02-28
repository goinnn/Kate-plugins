import compiler

import kate

from PyQt4 import QtCore


@kate.action('parse code', shortcut='Ctrl+6', menu='Edit')
def parseCode(doc=None):
    if doc and doc.isModified():
        return
    doc = doc or kate.activeDocument()
    text = unicode(doc.text())
    try:
        code = compiler.parse(text)
        kate.gui.popup("OK", 3, icon='dialog-ok', minTextWidth=200)
    except SyntaxError, e:
        treatmentException(e)


def treatmentException(e):
    f = e.filename or ''
    text = e.text
    line = e.lineno
    message = 'There was a syntax error in this file:'
    if f:
        message = '%s\n  * file: %s' % (message, f)
    if text:
        message = '%s\n  * text: %s' % (message, text)
    if line:
        message = '%s\n  * line: %s' % (message, line)
    kate.gui.popup(message, 10, icon='dialog-warning', minTextWidth=200)


def createSignalCheckDocument(view, *args, **kwargs):
    doc = view.document()
    doc.modifiedChanged.connect(parseCode)

windowInterface = kate.application.activeMainWindow()
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalCheckDocument)
