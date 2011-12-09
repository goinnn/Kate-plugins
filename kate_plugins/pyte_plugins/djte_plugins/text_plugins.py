import kate

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


@kate.action("template urls", shortcut="Ctrl+Alt+7",  menu='Edit')
def import_urls():
    currentDocument = kate.activeDocument()
    path = unicode(currentDocument.url().directory())
    path_split = path.split('/')
    application = path_split[len(path_split) - 1]
    insertText(TEXT_URLS % application)


@kate.action("import views", shortcut="Ctrl+Alt+v", menu='Edit')
def import_views():
    insertText(TEXT_VIEWS)
