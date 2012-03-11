import kate

from PyQt4 import QtCore

from kate_settings_plugins import KATE_ACTIONS, CHECKALL_TO_SAVE


def clearMarksOfError(doc, mark_iface):
    for line in range(doc.lines()):
        if mark_iface.mark(line) == mark_iface.Error:
            mark_iface.removeMark(line, mark_iface.Error)


def hideOldPopUps():
    mainWindow = kate.mainWindow()
    popups = kate.gui.TimeoutPassivePopup.popups.get(mainWindow, []) or []
    for popup in popups:
        popup.timer.stop()
        popup.hide()
        popup.setFixedHeight(0)
        popup.adjustSize()
        popup.originalHeight = popup.height()
        popup.offsetBottom = 0
        popup.move(0, 0)


@kate.action(**KATE_ACTIONS['checkAll'])
def checkAll(doc=None, excludes=None, exclude_all=False):
    from pyte_plugins.check_plugins.parse_plugins import parseCode
    if not doc or not doc.isModified():
        excludes = excludes or []
        currentDoc = doc or kate.activeDocument()
        mark_iface = currentDoc.markInterface()
        clearMarksOfError(currentDoc, mark_iface)
        hideOldPopUps()
        if not exclude_all:
            if not 'parseCode' in excludes:
                parseCode(currentDoc, refresh=False)
            if not 'checkPyflakes' in excludes:
                try:
                    from pyte_plugins.check_plugins.pyflakes_plugins import checkPyflakes
                    checkPyflakes(currentDoc, refresh=False)
                except ImportError:
                    pass
            if not 'checkPep8' in excludes:
                try:
                    from pyte_plugins.check_plugins.pep8_plugins import checkPep8
                    checkPep8(currentDoc, refresh=False)
                except ImportError:
                    pass
            if not 'checkJslint' in excludes:
                try:
                    from jste_plugins.jslint_plugins import checkJslint
                    checkJslint(currentDoc, refresh=False)
                except ImportError:
                    pass
        if not doc and currentDoc.isModified() and not excludes:
            kate.gui.popup('You must save the file first', 3,
                            icon='dialog-warning', minTextWidth=200)


def createSignalCheckDocument(view, *args, **kwargs):
    doc = view.document()
    doc.modifiedChanged.connect(checkAll)


if CHECKALL_TO_SAVE:
    windowInterface = kate.application.activeMainWindow()
    windowInterface.connect(windowInterface,
                            QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                            createSignalCheckDocument)
