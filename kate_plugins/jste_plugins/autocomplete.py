# -*- coding: utf-8 -*-
# Copyright (c) 2011 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import kate
import re

from PyQt4 import QtCore

from autopate import AbstractJSONFileCodeCompletionModel
from kate_settings_plugins import (JAVASCRIPT_AUTOCOMPLETE_ENABLED,
                                   JQUERY_AUTOCOMPLETE_ENABLED)


class StaticJSCodeCompletionModel(AbstractJSONFileCodeCompletionModel):

    MIMETYPES = ['application/javascript', 'text/html']
    TITLE_AUTOCOMPLETION = "JS Auto Complete"
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
    TITLE_AUTOCOMPLETION = "jQuery Auto Complete"
    FILE_PATH = 'jste_plugins/autocomplete_jquery.json'

    def __init__(self, *args, **kwargs):
        super(StaticJSCodeCompletionModel, self).__init__(*args, **kwargs)
        self.expr = re.compile('(?:.)*[$|jQuery]\(["|\']?(?P<dom_id>[\.\-_\w]+)["|\']?\)\.(?P<query>[\.\-_\w]+)*$')
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
