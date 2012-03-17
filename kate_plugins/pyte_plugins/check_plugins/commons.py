import kate

from PyKDE4.ktexteditor import KTextEditor

from kate_core_plugins import is_mymetype_python


def showOk(message="Ok", time=3, icon='dialog-ok'):
    kate.gui.popup(message, time, icon='dialog-ok', minTextWidth=200)


def generateErrorMessage(error, key_line='line', key_column='column', header=True):
    message = ''
    exclude_keys = [key_line, key_column, 'filename']
    line = error[key_line]
    column = error.get(key_column, None)
    if header or column:
        column = error.get(key_column, None)
        if column:
            message = '~*~ Position: (%s, %s)' % (line, column)
        else:
            message = '~*~ Line: %s' % line
        message += ' ~*~'
    for key, value in error.items():
        if value and key not in exclude_keys:
            if key != 'message':
                message = '%s\n     * %s: %s' % (message, key, value)
            else:
                message = '%s\n     %s' % (message, value)
    return message


def getErrorMessagesOrder(messages_items, max_errors, current_line=None, current_column=None):
    messages_order = []
    first_error = None
    num_messages = 0
    if not current_line:
        for line, message in messages_items:
            messages_order.extend(message)
            num_messages += 1
            if num_messages >= max_errors:
                break
        return (0, messages_order)
    for i, error in enumerate(messages_items):
        line, column = _uncompress_key(error[0])
        message = error[1]
        if line > current_line or (line == current_line and column > current_column):
            if first_error is None:
                first_error = i
            num_messages += 1
            messages_order.extend(message)
        if num_messages >= max_errors:
            break
    if len(messages_order) == max_errors:
        return (first_error, messages_order)
    for i, error in enumerate(messages_items):
        line, column = _uncompress_key(error[0])
        message = error[1]
        if line <= current_line:
            if first_error is None:
                first_error = i
            num_messages += 1
            messages_order.extend(message)
        else:
            break
        if num_messages >= max_errors:
            break
    return (first_error, messages_order)


def showErrors(message, errors, key_mark, doc, time=10, icon='dialog-warning',
               key_line='line', key_column='column',
               max_errors=3, show_popup=True, move_cursor=False):
    mark_iface = doc.markInterface()
    messages = {}
    view = kate.activeView()
    pos = view.cursorPosition()
    current_line = pos.line() + 1
    current_column = pos.column() + 1
    for error in errors:
        header = False
        line = error[key_line]
        column = error.get(key_column, 0)
        pos = _compress_key(line, column)
        if not messages.get(line, None):
            header = True
            messages[pos] = []
        error_message = generateErrorMessage(error, key_line, key_column, header)
        messages[pos].append(error_message)
        mark_iface.setMark(line - 1, mark_iface.Error)

    messages_items = messages.items()
    messages_items.sort()
    if move_cursor:
        first_error, messages_show = getErrorMessagesOrder(messages_items,
                                                           max_errors,
                                                           current_line,
                                                           current_column)
        line_to_move, column_to_move = _uncompress_key(messages_items[first_error][0])
        moveCursorTFirstError(line_to_move, column_to_move)
    else:
        first_error, messages_show = getErrorMessagesOrder(messages_items, max_errors)
    if show_popup:
        message = '%s\n%s' % (message, '\n'.join(messages_show))
        if len(messages_show) < len(errors):
            message += '\n\nAnd other errors'
        kate.gui.popup(message, time, icon, minTextWidth=300)


def _compress_key(line, column):
    doc = kate.activeDocument()
    cipher = len('%s' % doc.lines())
    key_template = '%%%sd' % cipher
    key_template += '__%3d'
    return key_template % (line, column)


def _uncompress_key(key):
    line, column = key.split('__')
    return (int(line), int(column))


def canCheckDocument(doc, text_plain=False):
    return not doc or (is_mymetype_python(doc, text_plain) and
                       not doc.isModified())


def moveCursorTFirstError(line, column=None):
    try:
        column = column or 0
        cursor = KTextEditor.Cursor(line - 1, column - 1)
        view = kate.activeView()
        view.setCursorPosition(cursor)
    except KeyError:
        pass
