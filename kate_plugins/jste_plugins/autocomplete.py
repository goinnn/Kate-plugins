import kate
import re

from PyQt4 import QtCore

from autopate import AbstractJSONFileCodeCompletionModel
from kate_settings_plugins import (JAVASCRIPT_AUTOCOMPLETE_ENABLED,
                                   JQUERY_AUTOCOMPLETE_ENABLED)


class StaticJSCodeCompletionModel(AbstractJSONFileCodeCompletionModel):

    MIMETYPES = ['application/javascript', 'text/html']
    TITLE_AUTOCOMPLETATION = "JS Auto Complete"
    # generated with jste_plugins/autocomplete_js.gen
    FILE_PATH = 'jste_plugins/autocomplete_js.json'
    OPERATORS = ["=", " ", "[", "]", "(", ")", "{", "}", ":", ">", "<",
                 "+", "-", "*", "/", "%", " && ", " || ", ","]

    def __init__(self, *args, **kwargs):
        super(StaticJSCodeCompletionModel, self).__init__(*args, **kwargs)
        self.json['window'] = {'icon': 'module', 'children': {}}

    def getLastExpression(self, line, operators=None):
        expr = super(StaticJSCodeCompletionModel, self).getLastExpression(line,
                                                           operators=operators)
        if expr.startswith("window."):
            expr = expr.replace('window.', '', 1)
        return expr


class StaticJQueryCompletionModel(StaticJSCodeCompletionModel):
    TITLE_AUTOCOMPLETATION = "jQuery Auto Complete"
    FILE_PATH = 'jste_plugins/autocomplete_jquery.json'

    def __init__(self, *args, **kwargs):
        super(StaticJSCodeCompletionModel, self).__init__(*args, **kwargs)
        self.expr = re.compile('(?:.)*[$|jQuery]\(["|\']?(?P<dom_id>\w+)["|\']?\)\.(?P<query>[\.\w]+)*$')
        self.object_jquery = False

    @classmethod
    def createItemAutoComplete(cls, text, *args, **kwargs):
        if text == '___object':
            return None
        return super(StaticJQueryCompletionModel, cls).createItemAutoComplete(text, *args, **kwargs)

    def getLastExpression(self, line, operators=None):
        m = self.expr.match(line)
        self.object_jquery = m
        if m:
            return m.groups()[1] or ''
        expr = super(StaticJSCodeCompletionModel, self).getLastExpression(line,
                                                           operators=operators)
        if expr.startswith("$."):
            expr = expr.replace('$.', 'jQuery.', 1)
        return expr

    def getJSON(self, lastExpression, line):
        if self.object_jquery:
            return self.json['___object']
        return self.json


def createSignalAutocompleteJS(view, *args, **kwargs):
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(jscodecompletationmodel)


def createSignalAutocompletejQuery(view, *args, **kwargs):
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(jquerycodecompletationmodel)


if JAVASCRIPT_AUTOCOMPLETE_ENABLED or JQUERY_AUTOCOMPLETE_ENABLED:
    windowInterface = kate.application.activeMainWindow()
    if JAVASCRIPT_AUTOCOMPLETE_ENABLED:
        jscodecompletationmodel = StaticJSCodeCompletionModel(windowInterface)
        windowInterface.connect(windowInterface,
                              QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                              createSignalAutocompleteJS)
    if JQUERY_AUTOCOMPLETE_ENABLED:
        jquerycodecompletationmodel = StaticJQueryCompletionModel(windowInterface)
        windowInterface.connect(windowInterface,
                              QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                              createSignalAutocompletejQuery)
