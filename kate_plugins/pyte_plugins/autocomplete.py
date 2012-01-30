import compiler
import glob
import os
import pkgutil
import re
import sys

import kate

from compiler import parse

from PyKDE4.ktexteditor import KTextEditor
from PyQt4 import QtCore
from PyQt4.QtCore import QModelIndex, Qt, QVariant
from pysmell.codefinder import CodeFinder


global modules_path
global python_path
global windowInterface
global codecompletationmodel
modules_path = {}
python_path = []

_spaces = "(?:\ |\t|\n)*"
_from = "%sfrom" % _spaces
_import = "%simport" % _spaces
_first_module = "(?P<firstmodule>\w+)"
_other_module = "(?:[.](?P<othermodule>[\w.]+)?)?"
_import_module = "(?P<importmodule>\w+)"

_from_begin = "%s%s" %(_from, _spaces)
_from_first_module = "%s%s" % (_from_begin, _first_module)
_from_other_modules = "%s%s" %(_from_first_module, _other_module)
_from_import = "%s%s%s" % (_from_other_modules, _spaces, _import)
_from_complete = "%s%s%s?" %(_from_import, _spaces, _import_module)

_import_begin = "%s" % _import
_import_complete = "%s%s%s?" %(_import_begin, _spaces, _import_module)

from_first_module = re.compile(_from_first_module + "?$")
from_other_modules = re.compile(_from_other_modules + "$")
from_import = re.compile(_from_import + "$")
from_complete = re.compile(_from_complete + "$")

import_begin = re.compile(_import_begin + "$")
import_complete = re.compile(_import_complete + "?$")


class PythonCodeCompletionModel(KTextEditor.CodeCompletionModel):

    def __init__(self, *args, **kwargs):
        super(PythonCodeCompletionModel, self).__init__(*args, **kwargs)
        self.resultList = []

    roles = {
        KTextEditor.CodeCompletionModel.CompletionRole:
            QVariant(
                KTextEditor.CodeCompletionModel.FirstProperty |
                KTextEditor.CodeCompletionModel.Public |
                KTextEditor.CodeCompletionModel.LastProperty |
                KTextEditor.CodeCompletionModel.Prefix),
        KTextEditor.CodeCompletionModel.ScopeIndex:
            QVariant(0),
        KTextEditor.CodeCompletionModel.MatchQuality:
            QVariant(10),
        KTextEditor.CodeCompletionModel.HighlightingMethod:
            QVariant(QVariant.Invalid),
        KTextEditor.CodeCompletionModel.InheritanceDepth:
            QVariant(0),
    }

    def completionInvoked(self, view, word, invocationType):
        is_auto = False
        line_start = word.start().line()
        line_end = word.end().line()
        self.resultList = []
        if line_start != line_end:
            return
        doc = view.document()
        line = unicode(doc.line(line_start))
        if not line:
            return
        if 'from' in line or 'import' in line:
            is_auto = self.autoCompleteImport(view, word, line)
        if not is_auto and '.' in line:
            is_auto = self.autoCompleteDynamic(view, word, line)

    def autoCompleteImport(self, view, word, line):
        mfb = from_first_module.match(line) or import_complete.match(line)
        if mfb:
            self.resultList = self.get_top_level_modules()
            return True
        mfom = from_other_modules.match(line)
        if mfom:
            module, submodules = mfom.groups()
            if not submodules:
                submodules = []
            else:
                submodules = submodules.split('.')[:-1]
            self.resultList = self.get_submodules(module,
                                                  submodules,
                                                  attributes=False)
            return True
        mfc = from_complete.match(line)
        if mfc:
            module, submodules, import_module = mfc.groups()
            submodules = submodules.split('.')
            self.resultList = self.get_submodules(module,
                                                  submodules,
                                                  attributes=True)
            return True
        return False

    def autoCompleteDynamic(self, view, word, line):
        last_dot = line.rindex('.')
        line = line[:last_dot]
        doc = view.document()
        text_list = unicode(doc.text()).split("\n")
        raw, column = word.start().position()
        del text_list[raw]
        text = '\n'.join(text_list)
        return self.getDynamic(text, line)

    def getDynamic(self, text, code_line):
        try:
            code = parse(text)
            code_walk = compiler.walk(code, CodeFinder())
            code_line_split = code_line.split('.')
            prefix = code_line_split[0]
            prfx = '__package____module__.'
            prfx_code_line = '%s%s' %(prfx, prefix)
            if prfx_code_line in code_walk.modules['CONSTANTS']:
                return False
            elif code_walk.modules['CLASSES'].get(prfx_code_line, None):
                class_smell = code_walk.modules['CLASSES'].get(prfx_code_line)
                resultList = [c[0] for c in class_smell['constructor']]
                resultList.extend([m[0] for m in class_smell['methods']])
                resultList.extend(class_smell['properties'])
                self.resultList = resultList
                return True
            elif code_walk.modules['POINTERS'].get(prfx_code_line, None):
                module_path = code_walk.modules['POINTERS'].get(prfx_code_line, None)
                module = module_path.split('.')[0]
                submodules = module_path.split('.')[1:]
                submodules.extend(code_line_split[1:])
                self.resultList = self.get_submodules(module,
                                                      submodules,
                                                      attributes=True)
                if not self.resultList and len(submodules) >=2:
                    module_path = modules_path[module][0] + os.sep + os.sep.join(submodules[:-2])
                    importer = pkgutil.get_importer(module_path)
                    module = importer.find_module(submodules[-2])
                    return self.getDynamic(module.get_source(), submodules[-1])
                return True
        except SyntaxError, e:
            kate.gui.popup('There was a syntax error in this file', 
                            2, icon='dialog-warning', minTextWidth=200)
        return False

    def index(self, row, column, parent):
        if (row < 0 or row >= len(self.resultList) or
            column < 0 or column >= KTextEditor.CodeCompletionModel.ColumnCount or
            parent.isValid()):
            return QModelIndex()
        return self.createIndex(row, column)

    def rowCount(self, parent):
        if parent.isValid():
            return 0 # Do not make the model look hierarchical
        else:
            return len(self.resultList)

    def data(self, index, role):
        if index.column() == KTextEditor.CodeCompletionModel.Name:
            if role == Qt.DisplayRole:
                return QVariant(self.resultList[index.row()])
            try:
                return self.roles[role]
            except KeyError:
                pass
        return QVariant()

    def executeCompletionItem(self, doc, word, row):
        return super(PythonCodeCompletionModel, self).executeCompletionItem(doc, word, row)

    @classmethod
    def get_pythonpath(cls):
        global python_path
        if python_path:
            return python_path
        python_path = sys.path
        try:
            from pyte_plugins import autocomplete_path
            python_path = autocomplete_path.path() + python_path
            sys.path = python_path
        except ImportError:
            pass
        return python_path

    @classmethod
    def get_top_level_modules(cls):
        # http://code.google.com/p/djangode/source/browse/trunk/djangode/data/codemodel/codemodel.py#57
        modules = []
        pythonpath = cls.get_pythonpath()
        for directory in pythonpath:
            for filename in glob.glob(directory + os.sep + "*"):
                module = None
                if filename.endswith(".py"):
                    module = filename.split(os.sep)[-1][:-3]
                elif os.path.isdir(filename) and os.path.exists(filename + os.sep + "__init__.py"):
                    module = filename.split(os.sep)[-1]
                if module and not module in modules:
                    modules.append(module)
                    modules_path[module] = [filename]
        return modules

    def get_submodules(self, module_name, submodules=None,
                       attributes=True):
        module_dir = modules_path[module_name][0]
        submodules = [submodule for submodule in submodules if submodule]
        if submodules:
            submodules = os.sep.join(submodules)
            module_dir = "%s%s%s" % (module_dir, os.sep, submodules)
        modules = []
        for loader, module_name, is_pkg in pkgutil.walk_packages([module_dir]):
            modules.append(module_name)
        if attributes:
            att_dir = os.sep.join(module_dir.split(os.sep)[:-1])
            att_module = module_dir.split(os.sep)[-1].replace('.py', '').replace('.pyc', '')
            importer = pkgutil.get_importer(att_dir)
            module = importer.find_module(att_module)
            if module:
                code = module.get_code()
                for const in code.co_consts:
                    if getattr(const, 'co_name', None):
                        modules.append(const.co_name)
        return sorted(modules)


def createSignalAutocompleteDocument(view, *args, **kwargs): 
    # https://launchpad.net/ubuntu/precise/+source/pykde4
    # https://launchpad.net/ubuntu/precise/+source/pykde4/4:4.7.97-0ubuntu1/+files/pykde4_4.7.97.orig.tar.bz2
    #http://doc.trolltech.com/4.6/qabstractitemmodel.html
    #http://gitorious.org/kate/kate/blobs/a17eb928f8133528a6194b7e788ab7a425ef5eea/ktexteditor/codecompletionmodel.cpp
    #http://code.google.com/p/lilykde/source/browse/trunk/frescobaldi/python/frescobaldi_app/mainapp.py#1391
    #http://api.kde.org/4.0-api/kdelibs-apidocs/kate/html/katecompletionmodel_8cpp_source.html
    #https://svn.reviewboard.kde.org/r/1640/diff/?expand=1
    PythonCodeCompletionModel.get_top_level_modules()
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(codecompletationmodel)

windowInterface = kate.application.activeMainWindow()
codecompletationmodel = PythonCodeCompletionModel(windowInterface)
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalAutocompleteDocument)
