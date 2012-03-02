import _ast

import kate
from pyflakes.checker import Checker
from pyflakes.messages import Message
from PyQt4 import QtCore

from kate_settings_plugins import kate_plugins_settings
from pyte_plugins.check_plugins import commons


def pyflakes(codeString, filename):
    """
    Check the Python source given by C{codeString} for flakes.
    """
    # First, compile into an AST and handle syntax errors.
    try:
        tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError, value:
        msg = value.args[0]
        lineno = value.lineno
        # If there's an encoding problem with the file, the text is None.
        if value.text is None:
            # Avoid using msg, since for the only known case, it contains a
            # bogus message that claims the encoding the file declared was
            # unknown.
            msg = "Problem decoding source"
            lineno = 1
        error = Message(filename, lineno)
        error.message = msg + "%s"
        error.message_args = ""
        return [error]
    else:
        # Okay, it's syntactically valid.  Now check it.
        w = Checker(tree, filename)
        w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
        return w.messages


@kate.action(**kate_plugins_settings['checkPyflakes'])
def checkPyflakes(currentDocument=None):
    if not commons.canCheckDocument(currentDocument):
        return
    currentDocument = currentDocument or kate.activeDocument()

    path = unicode(currentDocument.url().path())
    mark_key = '%s-pyflakes' % path

    text = unicode(currentDocument.text())
    errors = pyflakes(text.encode('utf-8'), path)
    errors_to_show = []

    if len(errors) == 0:
        commons.removeOldMarks(mark_key, currentDocument)
        commons.showOk("Pyflakes Ok")
        return

    # Prepare errors found for painting
    for error in errors:
        errors_to_show.append({
            "filename": path,
            "message": error.message % error.message_args,
            "line": error.lineno,
            })

    commons.showErrors('Pyflakes Errors:', errors_to_show, mark_key,
                       currentDocument)


def createSignalCheckDocument(view, *args, **kwargs):
    doc = view.document()
    doc.modifiedChanged.connect(checkPyflakes)

windowInterface = kate.application.activeMainWindow()
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalCheckDocument)
