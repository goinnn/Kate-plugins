# Inspirated in http://code.google.com/p/djangode/source/browse/trunk/djangode/gui/python_editor.py#214

import kate
from PyQt4 import QtCore, QtGui


class AutoCompleter(QtGui.QCompleter):

    def __init__(self, l, view):
        super(AutoCompleter, self).__init__(l, view)
        self.view = view

    def auto_insertText(self, text):
        self.view.insertText('.%s' % text)


def autocompleteDocument(*args, **kwargs):
    currentDocument = kate.activeDocument()
    print currentDocument.line(0)


def createSignalAutocompleteDocument(view, **kwargs):
    # https://launchpad.net/ubuntu/precise/+source/pykde4
    # https://launchpad.net/ubuntu/precise/+source/pykde4/4:4.7.97-0ubuntu1/+files/pykde4_4.7.97.orig.tar.bz2
    view.document().connect(view.document(),
                        QtCore.SIGNAL("textInserted (KTextEditor::Document*, const KTextEditor::Range&)"),
                        autocompleteDocument)
windowInterface = kate.application.activeMainWindow()
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalAutocompleteDocument)


@kate.action('autopate', shortcut='Ctrl+.', menu='Edit')
def autoPate():
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    word_list = ['contrib', 'auth', 'admin', 'forms',
                 'django.forms import ModelForm']

    string_list = QtCore.QStringList()
    for word in word_list:
        string_list.append(word)

    completer = AutoCompleter(QtCore.QStringList(), view)
    completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    completer.setModel(QtGui.QStringListModel(string_list, completer))
    completer.setCompletionPrefix('')
    completer.popup().setCurrentIndex(completer.completionModel().index(0, 0))

    point = view.cursorToCoordinate(currentPosition)
    point.setY((point.y() - 80))

    qr = QtCore.QRect(point, QtCore.QSize(100, 100))
    qr.setWidth(completer.popup().sizeHintForColumn(0)
              + completer.popup().verticalScrollBar().sizeHint().width())
    completer.setWidget(view)

    completer.activated.connect(completer.auto_insertText)
    completer.complete(qr)
