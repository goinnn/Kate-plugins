import kate
import re

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

TEXT_INIT =  """
    def __init__(self, *args, **kwargs):
        super(%s, self).__init__(*args, **kwargs)
"""

@kate.action('ipdb', shortcut='Ctrl+I', menu='Edit')
def insertIPDB():
    insertText("import ipdb; ipdb.set_trace()")


@kate.action('__init__', shortcut='Ctrl+-', menu='Edit')
def insertInit():
    class_name = 'XXX'
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    currentLine = currentPosition.line()
    pattern = re.compile("class (.*)\((.*)\):")
    while currentLine >= 0:
        text = unicode(currentDocument.line(currentLine))
        match = pattern.match(text)
        if match:
            class_name = match.groups()[0]
            break
        currentLine = currentLine -1
    insertText(TEXT_INIT % class_name)


@kate.action("import urls", shortcut="Ctrl+Alt+7",  menu='Edit')
def import_urls():
    currentDocument = kate.activeDocument()
    path = unicode(currentDocument.url().directory())
    path_split = path.split('/')
    application = path_split[len(path_split)-1]
    insertText(TEXT_URLS % application)


@kate.action("import views", shortcut="Ctrl+Alt+v", menu='Edit')
def import_views():
    insertText(TEXT_VIEWS)

