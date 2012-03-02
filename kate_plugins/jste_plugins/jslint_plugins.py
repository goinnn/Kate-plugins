import re

from pyjslint import check_JSLint
from pyte_plugins.check_plugins import commons
import kate


pattern = re.compile(r"Lint at line (\d+) character (\d+): (.*)")


@kate.action('JSLint', shortcut='Alt+J', menu='Edit')
def check_jslint():
    currentDocument = kate.activeDocument()
    path = unicode(currentDocument.url().path())

    errors = check_JSLint(currentDocument.text())
    errors_to_show = []

    # Paint errors found
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
        commons.showOk()
        return

    commons.showErrors(errors_to_show)
