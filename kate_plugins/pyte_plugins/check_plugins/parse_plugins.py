import compiler

import kate

from kate_settings_plugins import KATE_ACTIONS

from pyte_plugins.check_plugins.commons import (canCheckDocument, showOk,
                                                showErrors)
from pyte_plugins.check_plugins.check_all_plugins import checkAll


@kate.action(**KATE_ACTIONS['parseCode'])
def parseCode(doc=None, refresh=True, show_popup=True):
    if not canCheckDocument(doc):
        return
    if refresh:
        checkAll(doc, ['parseCode'], exclude_all=not doc)
    move_cursor = not doc
    doc = doc or kate.activeDocument()
    text = unicode(doc.text())
    text = text.encode('utf-8', 'ignore')
    mark_key = '%s-parse-python' % unicode(doc.url().path())
    try:
        compiler.parse(text)
        if show_popup:
            showOk('Parse code Ok')
    except SyntaxError, e:
        error = {}
        error['filename'] = e.filename
        error['text'] = e.text
        error['line'] = e.lineno
        showErrors('Parse code Errors:', [error], mark_key, doc,
                    show_popup=show_popup,
                    move_cursor=move_cursor)
