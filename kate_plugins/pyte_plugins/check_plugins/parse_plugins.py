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

import compiler

import kate

from kate_settings_plugins import KATE_ACTIONS

from pyte_plugins.check_plugins.commons import (canCheckDocument, showOk,
                                                showErrors)
from pyte_plugins.check_plugins.check_all_plugins import checkAll


@kate.action(**KATE_ACTIONS['parseCode'])
def parseCode(doc=None, refresh=True):
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
        showOk('Parse code Ok')
    except SyntaxError, e:
        error = {}
        error['filename'] = e.filename
        error['text'] = e.text
        error['line'] = e.lineno
        showErrors('Parse code Errors:', [error], mark_key, doc,
                    move_cursor=move_cursor)
