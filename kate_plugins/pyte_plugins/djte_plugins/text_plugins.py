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

from kate_core_plugins import insertText, TEXT_TO_CHANGE
from kate_settings_plugins import KATE_ACTIONS

TEXT_URLS = """from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('%(app)s.views',
    url(r'^$', '%(change)s', name='%(change)s'),
)
"""

TEXT_VIEWS = """from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
"""


@kate.action(**KATE_ACTIONS['importUrls'])
def importUrls():
    currentDocument = kate.activeDocument()
    path = unicode(currentDocument.url().directory())
    path_split = path.split('/')
    application = path_split[len(path_split) - 1] or TEXT_TO_CHANGE
    insertText(TEXT_URLS % {'app': application,
                            'change': TEXT_TO_CHANGE})


@kate.action(**KATE_ACTIONS['importViews'])
def importViews():
    insertText(TEXT_VIEWS)
