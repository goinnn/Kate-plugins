from jste_plugins.autocomplete import *
from jste_plugins.jquery_plugins import *
from jste_plugins.json_plugins import *
try:
    from jste_plugins.jslint_plugins import *
except ImportError:
    pass
try:
    from pyte_plugins.autocomplete.autocomplete import *
except ImportError:
    pass

from pyte_plugins.djte_plugins.class_plugins import *
from pyte_plugins.djte_plugins.text_plugins import *
from pyte_plugins.djte_plugins.block_plugins import *
from pyte_plugins.text_plugins import *
from pyte_plugins.check_plugins.parse_plugins import *

try:
    from pyte_plugins.check_plugins.cheack_all_plugins import *
except ImportError:
    pass
try:
    from pyte_plugins.check_plugins.pep8_plugins import *
except ImportError:
    pass

try:
    from pyte_plugins.check_plugins.pyflakes_plugins import *
except ImportError:
    pass

from xhtml_plugins.xml_plugins import *

