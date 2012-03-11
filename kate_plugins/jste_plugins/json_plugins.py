import kate
import simplejson
import pprint

from kate_core_plugins import insertText
from kate_settings_plugins import KATE_ACTIONS


#http://www.muhuk.com/2008/11/extending-kate-with-pate/
@kate.action(**KATE_ACTIONS['togglePrettyJsonFormat'])
def togglePrettyJsonFormat():
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    encoding = unicode(currentDocument.encoding())
    source = unicode(view.selectionText(), encoding).encode(encoding)
    if not source:
        kate.gui.popup('Select a json text', 2,
                       icon='dialog-warning',
                       minTextWidth=200)
    pp = pprint.PrettyPrinter(indent=1)
    try:
        target = pp.pformat(simplejson.loads(source))
        view.removeSelectionText()
        insertText(target.replace("'", '"'))
    except simplejson.JSONDecodeError:
        kate.gui.popup('This text is not a valid json text', 2,
                       icon='dialog-warning',
                       minTextWidth=200)
