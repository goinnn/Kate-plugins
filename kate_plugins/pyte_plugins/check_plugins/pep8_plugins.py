import sys

import kate
import pep8


from kate_settings_plugins import kate_plugins_settings
from pyte_plugins.check_plugins import commons
from pyte_plugins.check_plugins.check_all_plugins import checkAll


class StoreErrorsChecker(pep8.Checker):

    def __init__(self, *args, **kwargs):
        super(StoreErrorsChecker, self).__init__(*args, **kwargs)
        self.error_list = []

    def report_error(self, line_number, offset, text, check):
        """
        Store the error
        """
        self.file_errors += 1
        self.error_list.append([line_number, offset, text[0:4], text])

    def get_errors(self):
        """
        Get the errors, and reset the checker
        """
        result, self.error_list = self.error_list, []
        self.file_errors = 0
        return result


@kate.action(**kate_plugins_settings['checkPep8'])
def checkPep8(currentDocument=None, refresh=True, show_popup=True):
    if not commons.canCheckDocument(currentDocument):
        return
    if refresh:
        checkAll(currentDocument, ['checkPep8'],
                 exclude_all=not currentDocument)
    currentDocument = currentDocument or kate.activeDocument()
    if currentDocument.isModified():
        if show_popup:
            kate.gui.popup('You must save the file first', 3,
                           icon='dialog-warning', minTextWidth=200)
        return
    path = unicode(currentDocument.url().path())
    mark_key = '%s-pep8' % unicode(currentDocument.url().path())
    # Check the file for errors with PEP8
    sys.argv = [path]
    pep8.process_options([path])
    checker = StoreErrorsChecker(path)
    checker.check_all()
    errors = checker.get_errors()

    if len(errors) == 0:
        if show_popup:
            commons.showOk('Pep8 Ok')
        return

    errors_to_show = []

    # Paint errors found
    for error in errors:
        errors_to_show.append({
            "line": error[0],
            "column": error[1],
            "filename": path,
            "message": error[3],
            })
    commons.showErrors('Pep8 Errors:', errors_to_show,
                       mark_key, currentDocument, show_popup=show_popup)
