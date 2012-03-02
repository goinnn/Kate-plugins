import kate


def showOk():
    kate.gui.popup("OK", 3, icon='dialog-ok', minTextWidth=200)


def generateErrorMessage(error):
    message = 'There was an error in this file:'
    for key, value in error.items():
        if value:
            message = '%s\n * %s: %s' % (message, key, value)
    return message


def showErrors(errors, time=10, icon='dialog-warning'):
    message = ''
    for error in errors:
        message += '%s\n' % generateErrorMessage(error)
    kate.gui.popup(message, time, icon, minTextWidth=200)
