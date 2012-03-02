import compiler

import kate

from PyQt4 import QtCore

from kate_settings_plugins import kate_plugins_settings
from utils import is_mymetype_python
from pyte_plugins.check_plugins.commons import showOk, showErrors, canCheckDocument, removeOldMarks


@kate.action(**kate_plugins_settings['parseCode'])
def parseCode(doc=None):
    if not canCheckDocument(doc, text_plain=True):
        return
    doc = doc or kate.activeDocument()
    text = unicode(doc.text())
    mark_key = '%s-parse-python' % unicode(doc.url().path())
    try:
        code = compiler.parse(text)
        removeOldMarks(mark_key, doc)
        showOk('Parse code Ok')
    except SyntaxError, e:
        error = {}
        error['filename'] = e.filename
        error['text'] = e.text
        error['line'] = e.lineno
        showErrors('Parse code Errors:', [error], mark_key, doc)


def createSignalCheckDocument(view, *args, **kwargs):
    doc = view.document()
    doc.modifiedChanged.connect(parseCode)

windowInterface = kate.application.activeMainWindow()
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalCheckDocument)
