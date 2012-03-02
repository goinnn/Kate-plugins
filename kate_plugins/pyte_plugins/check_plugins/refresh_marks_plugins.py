import kate

from kate_settings_plugins import kate_plugins_settings

from pyte_plugins.check_plugins.parse_plugins import parseCode
from pyte_plugins.check_plugins.pep8_plugins import checkPep8
from jste_plugins.jslint_plugins import checkJslint


@kate.action(**kate_plugins_settings['refreshMarks'])
def refreshMarks():
    currentDocument = kate.activeDocument()
    mark_iface = currentDocument.markInterface()
    mark_iface.clearMarks()
    parseCode(currentDocument)
    checkPep8(currentDocument)
    checkJslint(currentDocument)