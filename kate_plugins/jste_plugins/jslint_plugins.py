import re

from pyjslint import check_JSLint
import kate

from pyte_plugins.check_plugins import commons


pattern = re.compile(r"Lint at line (\d+) character (\d+): (.*)")


@kate.action('JSLint', shortcut='Alt+J', menu='Edit')
def check_jslint():
    currentDocument = kate.activeDocument()
    path = unicode(currentDocument.url().path())

    text = unicode(currentDocument.text())
    errors = check_JSLint(text.encode('utf-8'))
    errors_to_show = []

    # Prepare errors found for painting
    for error in errors:
        matches = pattern.search(error)
        if matches:
            errors_to_show.append({
                "filename": path,
                "message": matches.groups()[2],
                "line": int(matches.groups()[0]),
                "column": int(matches.groups()[1]),
                })

    if len(errors_to_show) == 0:
        commons.showOk("JSLint Ok")
        return

    commons.showErrors('JSLint Errors:', errors_to_show, '%s-jslint' % path,
                       currentDocument)
