import kate

from PyKDE4 import kdeui
from PyKDE4.kdecore import KConfig, KConfigGroup
from PyKDE4.ktexteditor import KTextEditor

from PyQt4 import QtGui

TEXT_TO_CHANGE = 'XXX'


def insertText(text, strip_line=False,
               start_in_current_column=False,
               delete_spaces_initial=False,
               move_to=True):
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    spaces = ''
    if strip_line:
        text = '\n'.join([line.strip() for line in text.splitlines()])
    if start_in_current_column:
        number_of_spaces = currentPosition.position()[1]
        spaces = ' ' * number_of_spaces
        text = '\n'.join([i > 0 and '%s%s' % (spaces, line) or line
                            for i, line in enumerate(text.splitlines())])
    if delete_spaces_initial:
        currentPosition.setColumn(0)
    currentDocument.insertText(currentPosition, text)
    text_to_change_len = len(TEXT_TO_CHANGE)
    if move_to and TEXT_TO_CHANGE in text:
        currentPosition = view.cursorPosition()
        pos_xxx = text.index(TEXT_TO_CHANGE)
        lines = text[pos_xxx + text_to_change_len:].count('\n')
        column = len(text[:pos_xxx].split('\n')[-1]) - currentPosition.column()
        setSelectionFromCurrentPosition((-lines, column), (-lines, column + text_to_change_len))


def is_mymetype_python(doc, text_plain=False):
    mimetype = unicode(doc.mimeType())
    if mimetype == 'text/x-python':
        return True
    elif mimetype == 'text/plain' and text_plain:
        return True
    return False


def is_mymetype_js(doc, text_plain=False):
    mimetype = unicode(doc.mimeType())
    if mimetype == 'application/javascript':
        return True
    elif mimetype == 'text/plain' and text_plain:
        return True
    return False


def get_session():
    main_window = kate.mainWindow()
    title = unicode(main_window.windowTitle())
    session = None
    if title and title != 'Kate' and ":" in title:
        session = title.split(":")[0]
        if session == 'file':
            session = None
    if session:
        return session
    return get_last_session()


def get_last_session():
    config = KConfig('katerc')
    kgroup = KConfigGroup(config, "General")
    session = kgroup.readEntry("Last Session")
    if session:
        session = unicode(session)
        session = session.replace('.katesession', '')
        return session
    return None


def setSelectionFromCurrentPosition(start, end, pos=None):
    view = kate.activeView()
    pos = pos or view.cursorPosition()
    cursor1 = KTextEditor.Cursor(pos.line() + start[0], pos.column() + start[1])
    cursor2 = KTextEditor.Cursor(pos.line() + end[0], pos.column() + end[1])
    view.setSelection(KTextEditor.Range(cursor1, cursor2))
    view.setCursorPosition(cursor1)


def findMenu(menu_parent_slug):
    window = kate.mainWindow()
    for menu in window.findChildren(QtGui.QMenu):
        if str(menu.objectName()) == menu_parent_slug:
            return menu
    return None


def create_submenu(name_menu, slug_menu, menu_parent_slug):
    menu_parent = findMenu(menu_parent_slug)
    if not menu_parent:
        return ''
    window = kate.mainWindow()
    new_menu = kdeui.KMenu(name_menu, window)
    new_menu.setObjectName(slug_menu)

    action = QtGui.QAction(name_menu, new_menu)
    action.setObjectName(slug_menu)
    action.setMenu(new_menu)
    menu_parent.addAction(action)
    return slug_menu


def separated_menu(menu_parent_slug):
    menu_parent = findMenu(menu_parent_slug)
    action = QtGui.QAction('', None)
    menu_parent.insertSeparator(action)


def ipdb(with_position=True):
    import os
    import sys
    home = os.getenv("HOME")
    version = sys.version_info
    prefix = sys.prefix
    version = '%s%s' % (version[0], version[1])
    sys.path.insert(-1, os.path.join(prefix, 'lib/pymodules/python%s/IPython/Extensions' % version))
    sys.path.insert(-1, os.path.join(home, '.ipython'))
    sys.argv = [os.path.join(prefix, 'bin/ipython')]
    if with_position:
        currentDocument = kate.activeDocument()
        view = currentDocument.activeView()
        currentPosition = view.cursorPosition()
    import ipdb
    ipdb.set_trace()


def pdb():
    import pdb
    pdb.set_trace()
