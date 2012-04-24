import kate
import re
from kate_core_plugins import insertText
from kate_settings_plugins import KATE_ACTIONS, TEMPLATE_TAGS_CLOSE
from pyte_plugins.text_plugins import str_blank


@kate.action(**KATE_ACTIONS['closeTemplateTag'])
def closeTemplateTag():
    template_tags = '|'.join(TEMPLATE_TAGS_CLOSE)
    pattern_close = re.compile("(.)*{%%%(espaces)s(%(tags)s)%(espaces)s(.)*%(espaces)s%%}(.)*" % {'espaces': str_blank, 'tags': template_tags})
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    currentPosition = view.cursorPosition()
    currentLine = currentPosition.line()
    while currentLine >= 0:
        text = unicode(currentDocument.line(currentLine))
        match = pattern_close.match(text)
        if match:
            tag = match.groups()[1]
            print match.groups()
            break
        currentLine = currentLine - 1
    insertText("{%% end%s %%}" % tag)


@kate.action(**KATE_ACTIONS['createBlock'])
def createBlock():
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    encoding = unicode(currentDocument.encoding())
    source = unicode(view.selectionText(), encoding).encode(encoding)
    try:
        block_type, block_source = source.split("#")
    except ValueError:
        block_type = 'block'
        block_source = source
    view.removeSelectionText()
    insertText("{%% %(block_type)s %(block_source)s %%}XXX{%% end%(block_type)s %%}" %
                {'block_type': block_type, 'block_source': block_source})
