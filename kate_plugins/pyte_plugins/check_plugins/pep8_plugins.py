import kate
import sys

import pep8

import commons


old_marks = {}


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


@kate.action('pep8', shortcut='Alt+8', menu='Edit')
def check_pep8():
    currentDocument = kate.activeDocument()
    mark_iface = currentDocument.markInterface()
    path = unicode(currentDocument.url().path())

    # Check the file for errors with PEP8
    sys.argv = [path]
    pep8.process_options([path])
    checker = StoreErrorsChecker(path)
    checker.check_all()
    errors = checker.get_errors()

    # Delete previous errors
    if path in old_marks:
        for mark in old_marks[path]:
            mark_iface.removeMark(mark.line, mark.type)
    old_marks[path] = []

    if len(errors) == 0:
        commons.showOk()
        return

    errors_to_show = []

    # Paint errors found
    for error in errors:
        mark = kate.KTextEditor.Mark()
        mark.line = error[0] - 1
        mark.type = mark_iface.Error
        mark_iface.setMark(mark.line, mark.type)
        old_marks[path].append(mark)
        errors_to_show.append({
            "line": error[0],
            "column": error[1],
            "filename": path,
            "message": error[3],
            })

    commons.showErrors(errors_to_show)
