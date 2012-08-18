# -*- coding: utf-8 -*-
# Copyright (c) 2011 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

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
