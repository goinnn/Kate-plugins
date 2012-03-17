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
