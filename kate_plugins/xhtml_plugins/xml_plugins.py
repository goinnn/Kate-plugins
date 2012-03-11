import kate
from xml.dom import minidom
from xml.parsers.expat import ExpatError
from kate_core_plugins import insertText
from kate_settings_plugins import KATE_ACTIONS


@kate.action(**KATE_ACTIONS['togglePrettyXMLFormat'])
def togglePrettyJsonFormat():
    currentDocument = kate.activeDocument()
    view = currentDocument.activeView()
    source = unicode(view.selectionText()).encode('utf-8', 'ignore')
    if not source:
        kate.gui.popup('Select a xml text', 2,
                       icon='dialog-warning',
                       minTextWidth=200)
    try:
        target = minidom.parseString(source)
        view.removeSelectionText()
        xml_pretty = target.toprettyxml()
        xml_pretty = '\n'.join([line for line in xml_pretty.split("\n") if line.replace(' ', '').replace('\t', '')])
        insertText(xml_pretty)
    except ExpatError:
        kate.gui.popup('This text is not a valid xml text', 2,
                       icon='dialog-warning',
                       minTextWidth=200)
