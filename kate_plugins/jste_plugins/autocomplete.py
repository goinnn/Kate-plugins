import kate

from PyQt4 import QtCore

from autopate import AbstractJSONFileCodeCompletionModel


class StaticJSCodeCompletionModel(AbstractJSONFileCodeCompletionModel):

    MIMETYPES = ['js', 'html', 'htm']
    # generated with jste_plugins/autocomplete_js.gen
    FILE_PATH = 'jste_plugins/autocomplete_js.json'
    OPERATORS = ["=", " ", "[", "]", "(", ")", "{", "}", ":", ">", "<",
                 "+", "-", "*", "/", "%", " && ", " || ", ","]


def createSignalAutocompleteDocument(view, *args, **kwargs):
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(jscodecompletationmodel)


windowInterface = kate.application.activeMainWindow()
jscodecompletationmodel = StaticJSCodeCompletionModel(windowInterface)
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalAutocompleteDocument)
