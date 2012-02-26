import re


_spaces = "(?:\ |\t|\n)*"
# "   from"
_from = "%sfrom" % _spaces
# "   import"
_import = "%simport" % _spaces
_first_module = "(?P<firstmodule>\w+)"
_other_module = "(?:[.](?P<othermodule>[\w.]+)?)?"
_import_module = "(?:\w+,(?:\ |\t|\n)*)*(?P<importmodule>\w+)"

# "   from   "
_from_begin = "%s%s" % (_from, _spaces)
# "   from   os"
_from_first_module = "%s%s" % (_from_begin, _first_module)
# "   from   os.path"
_from_other_modules = "%s%s" % (_from_first_module, _other_module)
# "   from   os.path import"
_from_import = "%s%s%s" % (_from_other_modules, _spaces, _import)
# "   from   os.path import join"
_from_complete = "%s%s%s?" % (_from_import, _spaces, _import_module)

# "   import"
_import_begin = "%s" % _import
# "   import   os"
_import_complete = "%s%s%s?" % (_import_begin, _spaces, _import_module)

from_first_module = re.compile(_from_first_module + "?$")
from_other_modules = re.compile(_from_other_modules + "$")
from_import = re.compile(_from_import + "$")
from_complete = re.compile(_from_complete + "$")

import_begin = re.compile(_import_begin + "$")
import_complete = re.compile(_import_complete + "?$")
