import kate
import simplejson
import pprint
import utils

from simplejson import JSONDecodeError


#http://www.muhuk.com/2008/11/extending-kate-with-pate/
@kate.action('Pretty Json', shortcut='Ctrl+Alt+J', menu='Edit')
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
        utils.insertText(target)
    except JSONDecodeError:
        kate.gui.popup('This text is not a valid json text', 2,
                       icon='dialog-warning',
                       minTextWidth=200)
