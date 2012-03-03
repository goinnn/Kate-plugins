import re

import kate

from pyjslint import check_JSLint

from utils import is_mymetype_js

from kate_settings_plugins import kate_plugins_settings
from pyte_plugins.check_plugins import commons
from pyte_plugins.check_plugins.check_all_plugins import checkAll


pattern = re.compile(r"Lint at line (\d+) character (\d+): (.*)")


@kate.action(**kate_plugins_settings['checkJslint'])
def checkJslint(currentDocument=None, refresh=True, show_popup=True):
    if not (not currentDocument or (is_mymetype_js(currentDocument) and
                                    not currentDocument.isModified())):
        return
    if refresh:
        checkAll(currentDocument, ['checkJslint'],
                 exclude_all=not currentDocument)
    currentDocument = currentDocument or kate.activeDocument()
    path = unicode(currentDocument.url().path())
    mark_key = '%s-jslint' % path

    text = unicode(currentDocument.text())
    errors = check_JSLint(text.encode('utf-8', 'ignore'))
    errors_to_show = []

    # Prepare errors found for painting
    for error in errors:
        matches = pattern.search(error)
        if matches:
            errors_to_show.append({
                "filename": path,
                "message": matches.groups()[2],
                "line": int(matches.groups()[0]) - 1,
                "column": int(matches.groups()[1]),
                })

    if len(errors_to_show) == 0:
        if show_popup:
            commons.showOk("JSLint Ok")
        return

    commons.showErrors('JSLint Errors:', errors_to_show, mark_key,
                       currentDocument, show_popup=show_popup)
