import kate
from PyQt4 import QtCore, QtGui


@kate.action('autopate', shortcut='Ctrl+.', menu='Edit')
def autoPate():
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()

    word_list = ['contrib', 'auth', 'admin', 'forms', 'django.forms import ModelForm']

    string_list = QtCore.QStringList()
    for word in word_list:
        string_list.append(word)

    completer = QtGui.QCompleter(QtCore.QStringList(), view)
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

    completer.activated.connect(view.insertText)
    completer.complete(qr)

