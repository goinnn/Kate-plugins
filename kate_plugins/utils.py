import kate


def insertText(text, strip_line=False,
               start_in_current_column=False,
               delete_spaces_initial=False):
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
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


def ipdb(with_position=True):
    import sys
    sys.path.insert(-1, '/usr/lib/pymodules/python2.6/IPython/Extensions')
    sys.path.insert(-1, '/home/pmartin/.ipython')
    sys.argv = ['/usr/bin/ipython']
    if with_position:
        currentDocument = kate.activeDocument()
        view = currentDocument.activeView()
        currentPosition = view.cursorPosition()
    import ipdb
    ipdb.set_trace()


def pdb():
    import pdb
    pdb.set_trace()
