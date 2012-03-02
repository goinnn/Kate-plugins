import kate

from kate_settings_plugins import kate_plugins_settings
from utils import insertText

TEXT_URLS = """from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('%s.views',
    url(r'^$', 'XXX', name='XXX'),
)
"""

TEXT_VIEWS = """from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
"""


@kate.action(**kate_plugins_settings['importUrls'])
def importUrls():
    currentDocument = kate.activeDocument()
    path = unicode(currentDocument.url().directory())
    path_split = path.split('/')
    application = path_split[len(path_split) - 1]
    insertText(TEXT_URLS % application)


@kate.action(**kate_plugins_settings['importViews'])
def importViews():
    insertText(TEXT_VIEWS)
