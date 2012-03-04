import kate

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
               key_line='line', max_errors=3, show_popup=True):
    mark_iface = doc.markInterface()
    for i, error in enumerate(errors):
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
