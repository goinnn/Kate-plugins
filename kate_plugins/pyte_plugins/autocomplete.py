# Inspirated in http://code.google.com/p/djangode/source/browse/trunk/djangode/gui/python_editor.py#214
import os
import glob
import string
import sys

import kate

from PyQt4 import QtCore, QtGui


class AutoCompleter(QtGui.QCompleter):

    def __init__(self, l, view, activate_subfix):
        super(AutoCompleter, self).__init__(l, view)
        self.view = view
        self.activate_subfix = activate_subfix

    def auto_insertText(self, text):
        text = text.replace(self.completionPrefix(), '')
        self.view.insertText('%s%s'% (text, self.activate_subfix))

    @classmethod
    def get_top_level_modules(self):
        # http://code.google.com/p/djangode/source/browse/trunk/djangode/data/codemodel/codemodel.py#57
        modules = []
        pythonpath = sys.path
        for directory in pythonpath:
            for filename in glob.glob(directory + os.sep + "*"):
                module = None
                if filename.endswith(".py"):
                    module = filename.split(os.sep)[-1][:-3]
                elif os.path.isdir(filename) and os.path.exists(filename + os.sep + "__init__.py"):
                    module = filename.split(os.sep)[-1]
                if module and not module in modules:
                    modules.append(module)
        return sorted(modules)


class ComboBox(QtGui.QComboBox):

    def __init__(self, view, *args, **kwargs):
        super(ComboBox, self).__init__(view, *args, **kwargs)
        self.main_view = view

    def keyPressEvent(self, event, *args, **kwargs):
        key = unicode(event.text())
        if key in unicode(string.ascii_letters):
            self.main_view.insertText(event.text())
        return super(ComboBox, self).keyPressEvent(event, *args, **kwargs)


def autocompleteDocument(document, qrange, *args, **kwargs):
    line = unicode(document.line(qrange.start().line()))
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    activate_subfix = ''
    if line.lstrip().startswith("import "):
        auto_trigger = False
        #completion_func = setup_module_completion
    elif line.lstrip().startswith("from ") and " import " in line:
        auto_trigger = False
        #completion_func = setup_module_attribute_completion
    elif line.lstrip().startswith("from "):
        auto_trigger = True
        prefix = line.replace('from ', '')
        activate_subfix = '.'
        #completion_func = setup_module_completion
    #elif event.text() == ".":
        #auto_trigger = True
        #completion_func = setup_attribute_completion
    #elif event.text() == "(":
        #return display_tooltip(line, event)
    #elif event.text() == ")":
        #return hide_tooltip(line, event)
    else:
        auto_trigger = False
        #completion_func = setup_attribute_completion

    if not auto_trigger:
        return

    word_list = AutoCompleter.get_top_level_modules()

    string_list = QtCore.QStringList()
    for word in word_list:
        string_list.append(word)

    completer = AutoCompleter(QtCore.QStringList(), view, activate_subfix)
    completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    completer.setModel(QtGui.QStringListModel(string_list, completer))
    completer.setCompletionPrefix(prefix)
    completer.popup().setCurrentIndex(completer.completionModel().index(0, 0))

    point = view.cursorToCoordinate(currentPosition)
    point.setY((point.y() - 80))

    qr = QtCore.QRect(point, QtCore.QSize(100, 100))
    qr.setWidth(completer.popup().sizeHintForColumn(0)
              + completer.popup().verticalScrollBar().sizeHint().width())

    qcombo = ComboBox(view)
    completer.setWidget(qcombo)
    completer.activated.connect(completer.auto_insertText)
    completer.complete(qr)


def createSignalAutocompleteDocument(view, *args, **kwargs):
    # https://launchpad.net/ubuntu/precise/+source/pykde4
    # https://launchpad.net/ubuntu/precise/+source/pykde4/4:4.7.97-0ubuntu1/+files/pykde4_4.7.97.orig.tar.bz2
    view.document().textInserted.connect(autocompleteDocument)

windowInterface = kate.application.activeMainWindow()
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalAutocompleteDocument)
