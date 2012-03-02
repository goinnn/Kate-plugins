import kate

from utils import is_mymetype_python

old_marks = {}

def showOk(message="Ok", time=3, icon='dialog-ok'):
    kate.gui.popup(message, time, icon='dialog-ok', minTextWidth=200)


def generateErrorMessage(error):
    message = 'There was an error in this file:'
    for key, value in error.items():
        if value:
            message = '%s\n * %s: %s' % (message, key, value)
    return message


def showErrors(errors, key_mark, doc, time=10, icon='dialog-warning', key_line='line'):
    # Delete previous errors
    mark_iface = doc.markInterface()
    if key_mark in old_marks:
        for mark in old_marks[key_mark]:
            mark_iface.removeMark(mark.line, mark.type)
    old_marks[key_mark] = []

    message = ''
    for error in errors:
        message += '%s\n' % generateErrorMessage(error)
        mark = kate.KTextEditor.Mark()
        mark.line = error[key_line]
        mark.type = mark_iface.Error
        mark_iface.setMark(mark.line, mark.type)
        old_marks[key_mark].append(mark)
    kate.gui.popup(message, time, icon, minTextWidth=200)


def canCheckDocument(doc, text_plain=False):
    return not doc or (is_mymetype_python(doc, text_plain) and not doc.isModified())
