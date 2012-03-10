import kate

from PyKDE4.ktexteditor import KTextEditor

from utils import is_mymetype_python


def showOk(message="Ok", time=3, icon='dialog-ok'):
    kate.gui.popup(message, time, icon='dialog-ok', minTextWidth=200)


def generateErrorMessage(error):
    message = ''
    for key, value in error.items():
        if value:
            message = '%s\n * %s: %s' % (message, key, value)
    return message


def showErrors(message, errors, key_mark, doc, time=10, icon='dialog-warning',
               key_line='line', key_column='column',
               max_errors=3, show_popup=True, move_cursor=False):
    mark_iface = doc.markInterface()
    for i, error in enumerate(errors):
        if i == 0 and move_cursor:
            moveCursorTFirstError(error, key_line, key_column)
        if i < max_errors:
            message += '%s\n' % generateErrorMessage(error)
        elif i == max_errors:
            message += '\n And others'
        mark_iface.setMark(error[key_line] - 1, mark_iface.Error)
    if show_popup:
        kate.gui.popup(message, time, icon, minTextWidth=200)


def canCheckDocument(doc, text_plain=False):
    return not doc or (is_mymetype_python(doc, text_plain) and
                       not doc.isModified())


def moveCursorTFirstError(error, key_line='line', key_column='column'):
    try:
        cursor = KTextEditor.Cursor(error[key_line] - 1, error.get(key_column, 0))
        view = kate.activeView()
        view.setCursorPosition(cursor)
    except KeyError:
        pass
