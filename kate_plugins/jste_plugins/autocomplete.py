import kate

from PyQt4 import QtCore

from autopate import AbstractJSONFileCodeCompletionModel
from kate_settings_plugins import JAVASCRIPT_AUTOCOMPLETE_ENABLED


class StaticJSCodeCompletionModel(AbstractJSONFileCodeCompletionModel):

    MIMETYPES = ['js', 'html', 'htm']
    # generated with jste_plugins/autocomplete_js.gen
    FILE_PATH = 'jste_plugins/autocomplete_js.json'
    OPERATORS = ["=", " ", "[", "]", "(", ")", "{", "}", ":", ">", "<",
                 "+", "-", "*", "/", "%", " && ", " || ", ","]


def createSignalAutocompleteDocument(view, *args, **kwargs):
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(jscodecompletationmodel)

if JAVASCRIPT_AUTOCOMPLETE_ENABLED:
    windowInterface = kate.application.activeMainWindow()
    jscodecompletationmodel = StaticJSCodeCompletionModel(windowInterface)
    windowInterface.connect(windowInterface,
                            QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                            createSignalAutocompleteDocument)
