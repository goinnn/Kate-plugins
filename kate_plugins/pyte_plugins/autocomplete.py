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
from pysmell.codefinder import CodeFinder

from autopate import AbstractCodeCompletionModel

global modules_path
global python_path
global windowInterface
global codecompletationmodel
modules_path = {}
python_path = []

PYSMELL_PREFIX = '__package____module__.'

_spaces = "(?:\ |\t|\n)*"
_from = "%sfrom" % _spaces
_import = "%simport" % _spaces
_first_module = "(?P<firstmodule>\w+)"
_other_module = "(?:[.](?P<othermodule>[\w.]+)?)?"
_import_module = "(?:\w+,(?:\ |\t|\n)*)*(?P<importmodule>\w+)"

_from_begin = "%s%s" % (_from, _spaces)
_from_first_module = "%s%s" % (_from_begin, _first_module)
_from_other_modules = "%s%s" % (_from_first_module, _other_module)
_from_import = "%s%s%s" % (_from_other_modules, _spaces, _import)
_from_complete = "%s%s%s?" % (_from_import, _spaces, _import_module)

_import_begin = "%s" % _import
_import_complete = "%s%s%s?" % (_import_begin, _spaces, _import_module)

from_first_module = re.compile(_from_first_module + "?$")
from_other_modules = re.compile(_from_other_modules + "$")
from_import = re.compile(_from_import + "$")
from_complete = re.compile(_from_complete + "$")

import_begin = re.compile(_import_begin + "$")
import_complete = re.compile(_import_complete + "?$")


class PythonCodeCompletionModel(AbstractCodeCompletionModel):

    MIMETYPES = ['', 'py', 'pyc']
    OPERATORS = ["=", " ", "[", "]", "(", ")", "{", "}", ":", ">", "<",
                 "+", "-", "*", "/", "%", " and ", " or ", ","]

    def completionInvoked(self, view, word, invocationType):
        line = super(PythonCodeCompletionModel, self).completionInvoked(view,
                                                                        word,
                                                                        invocationType)
        is_auto = False
        line_rough = line
        if 'from' in line or 'import' in line:
            is_auto = self.autoCompleteImport(view, word, line)
        line = self.get_expression_last_expression(line)
        if not is_auto and line:
            is_auto = self.autoCompleteDynamic(view, word, line)
        if not is_auto and line and line_rough and not self.SEPARATOR in line_rough:
            is_auto = self.autoCompleteInThisFile(view, word, line)

    def executeCompletionItem(self, doc, word, row):
        raw, col = word.start().position()
        line = unicode(doc.line(raw))
        line = self.parse_line(line)
        t = self.resultList[row].get('type', None)
        args = self.resultList[row].get('args', None).strip()
        text = self.resultList[row].get('text', None)
        if not "from" in line and not "import" in line and \
           t in ['function', 'class']:
            if args == '()':
                doc.replaceText(word, '%s()' % text)
                return
            else:
                doc.replaceText(word, '%s(' % text)
                return
        return super(PythonCodeCompletionModel, self).executeCompletionItem(doc, word, row)

    def autoCompleteImport(self, view, word, line):
        mfb = from_first_module.match(line) or import_complete.match(line)
        if mfb:
            self.resultList = self.getTopLevelModules()
            return True
        mfom = from_other_modules.match(line)
        if mfom:
            module, submodules = mfom.groups()
            if not submodules:
                submodules = []
            else:
                submodules = submodules.split(self.SEPARATOR)[:-1]
            self.resultList = self.getSubmodules(module,
                                                  submodules,
                                                  attributes=False)
            return True
        mfc = from_complete.match(line)
        if mfc:
            module, submodules, import_module = mfc.groups()
            if submodules:
                submodules = submodules.split(self.SEPARATOR)
            else:
                submodules = []
            self.resultList = self.getSubmodules(module,
                                                  submodules,
                                                  attributes=True)
            return True
        return False

    def autoCompleteDynamic(self, view, word, line):
        try:
            last_dot = line.rindex(self.SEPARATOR)
            line = line[:last_dot]
        except ValueError:
            pass
        text = self._parse_text(view, word, line)
        return self.getDynamic(text, line)

    def autoCompleteInThisFile(self, view, word, line):
        text = self._parse_text(view, word, line)
        return self.getTextInfo(text, self.resultList)

    def parse_line(self, line):
        line = super(PythonCodeCompletionModel, self).parse_line(line)
        if "'" in line or '"' in line:
            return line
        if ";" in line:
            return self.parse_line(line.split(";")[-1])
        return line

    def _parse_text(self, view, word, line):
        doc = view.document()
        text_list = unicode(doc.text()).split("\n")
        raw, column = word.start().position()
        line = text_list[raw]
        if ";" in line and not "'" in line and not '"' in line:
            text_list[raw] = ';'.join(text_list[raw].split(";")[:-1])
        else:
            del text_list[raw]
        text = '\n'.join(text_list)
        line = line.strip()
        return text

    @classmethod
    def getTopLevelModules(cls):
        # http://code.google.com/p/djangode/source/browse/trunk/djangode/data/codemodel/codemodel.py#57
        modules = []
        pythonpath = cls.getPythonPath()
        for directory in pythonpath:
            for filename in glob.glob(directory + os.sep + "*"):
                module_name = None
                if filename.endswith(".py"):
                    module_name = filename.split(os.sep)[-1][:-3]
                    icon = 'module'
                elif os.path.isdir(filename) and os.path.exists(filename + os.sep + "__init__.py"):
                    module_name = filename.split(os.sep)[-1]
                    icon = 'package'
                if not module_name:
                    continue
                module = cls.createItemAutoComplete(module_name, icon)
                if module and not module in modules:
                    modules.append(module)
                    modules_path[module_name] = [filename]
        return modules

    def getSubmodules(self, module_name, submodules=None,
                       attributes=True):
        module_dir = modules_path[module_name][0]
        submodules = [submodule for submodule in submodules if submodule]
        if submodules:
            submodules = os.sep.join(submodules)
            module_dir = "%s%s%s" % (module_dir, os.sep, submodules)
        modules = []
        for loader, module_name, is_pkg in pkgutil.walk_packages([module_dir]):
            icon = is_pkg and 'package' or 'module'
            module = self.createItemAutoComplete(module_name, icon)
            modules.append(module)
        if attributes:
            att_dir = os.sep.join(module_dir.split(os.sep)[:-1])
            att_module = module_dir.split(os.sep)[-1].replace('.py', '').replace('.pyc', '')
            importer = pkgutil.get_importer(att_dir)
            module = importer.find_module(att_module)
            if module:
                self.getTextInfo(module.get_source(), modules)
        return sorted(modules)

    def getModuleSmart(self, module_name, submodules, submodules_undone=None):
        module_dir = modules_path[module_name][0]
        submodules_undone = submodules_undone or []
        submodules_str = os.sep.join(submodules)
        if submodules_str:
            module_dir = "%s%s%s" % (module_dir, os.sep, submodules_str)
        att_dir = os.sep.join(module_dir.split(os.sep)[:-1])
        att_module = module_dir.split(os.sep)[-1].replace('.py', '').replace('.pyc', '')
        importer = pkgutil.get_importer(att_dir)
        module = importer.find_module(att_module)
        if module:
            return (module, submodules_undone)
        elif submodules:
            submodules_undone.append(submodules[-1])
            return self.getModuleSmart(module_name, submodules[:-1], submodules_undone)
        return (None, submodules_undone)

    def getDynamic(self, text, code_line, text_info=True):
        try:
            code = parse(text)
            code_walk = compiler.walk(code, CodeFinder())
            code_line_split = code_line.split(self.SEPARATOR)
            prefix = code_line_split[0]
            prfx_code_line = '%s%s' % (PYSMELL_PREFIX, prefix)
            if prfx_code_line in code_walk.modules['CONSTANTS']:
                return False
            elif code_walk.modules['CLASSES'].get(prfx_code_line, None) and not code_line_split[1:]:
                class_smell = code_walk.modules['CLASSES'].get(prfx_code_line)
                self.treatment_pysmell_into_cls(class_smell, self.resultList)
                return True
            elif prfx_code_line in [name for name, args, desc in code_walk.modules['FUNCTIONS']]:
                index_func = [f[0] for f in code_walk.modules['FUNCTIONS']].index(prfx_code_line)
                func_smell = code_walk.modules['FUNCTIONS'][index_func]
                self.resultList.append(self.treatment_pysmell_into_func(func_smell))
                return True
            elif code_walk.modules['POINTERS'].get(prfx_code_line, None):
                module_path = code_walk.modules['POINTERS'].get(prfx_code_line, None)
                module = module_path.split(self.SEPARATOR)[0]
                submodules = module_path.split(self.SEPARATOR)[1:]
                submodules.extend(code_line_split[1:])
                module_done, submodules_undone = self.getModuleSmart(module, submodules)
                if not submodules_undone:
                    autocompletion_submodules = self.getSubmodules(module, submodules, True)
                    for autocompletion_submodule in autocompletion_submodules:
                        if autocompletion_submodule not in self.resultList:
                            self.resultList.append(autocompletion_submodule)
                submodules_undone.reverse()
                line = self.SEPARATOR.join(submodules_undone)
                text = module_done.get_source()
                if line:
                    return self.getDynamic(text, line)
                if text_info:
                    return self.getTextInfo(text, self.resultList)
        except SyntaxError, e:
            self.treatment_exception(e)
        return False

    @classmethod
    def getPythonPath(cls):
        global python_path
        if python_path:
            return python_path
        python_path = sys.path
        try:
            from pyte_plugins import autocomplete_path
            doc = kate.activeDocument()
            view = doc.activeView()
            python_path = autocomplete_path.path(doc, view) + python_path
            sys.path = python_path
        except ImportError:
            pass
        return python_path

    def getTextInfo(self, text, list_autocomplete, line=None):
        try:
            code = parse(text)
            code_walk = compiler.walk(code, CodeFinder())
            modules = code_walk.modules
            constans = modules['CONSTANTS']
            for constant in constans:
                item = self.treatment_pysmell_const(constant)
                if not item in list_autocomplete:
                    list_autocomplete.append(item)

            functions = modules['FUNCTIONS']
            for func in functions:
                item = self.treatment_pysmell_func(func)
                if not item in list_autocomplete:
                    list_autocomplete.append(item)

            classes = modules['CLASSES']
            for cls in classes.items():
                item = self.treatment_pysmell_cls(cls)
                if not item in list_autocomplete:
                    list_autocomplete.append(item)

            is_auto = len(list_autocomplete) > 0
            if not is_auto and line:
                line = "%s%s" % (PYSMELL_PREFIX, line.strip())
                for pointer in modules['POINTERS'].keys():
                    if pointer.startswith(line):
                        is_auto = is_auto or self.getDynamic(text,
                                        pointer.replace(PYSMELL_PREFIX, ''),
                                        text_info=False)
            return is_auto
        except SyntaxError, e:
            self.treatment_exception(e)
        return False

    def treatment_exception(self, e):
        if self.invocationType == KTextEditor.CodeCompletionModel.AutomaticInvocation:
            return
        f = e.filename or ''
        text = e.text
        line = e.lineno
        message = 'There was a syntax error in this file:'
        if f:
            message = '%s\n  * file: %s' % (message, f)
        if text:
            message = '%s\n  * text: %s' % (message, text)
        if line:
            message = '%s\n  * line: %s' % (message, line)
        kate.gui.popup(message,
                       2, icon='dialog-warning', minTextWidth=200)

    def treatment_pysmell_const(self, constant):
        constant = constant.replace(PYSMELL_PREFIX, '')
        return self.createItemAutoComplete(constant, 'constant')

    def treatment_pysmell_func(self, func):
        func_name, args, description = func
        func_name = func_name.replace(PYSMELL_PREFIX, '')
        args = ', '.join(args)
        args = ' (%s)' % args
        return self.createItemAutoComplete(func_name,
                                           'function', args, description)

    def treatment_pysmell_into_func(self, func):
        return self.treatment_pysmell_func(func)

    def treatment_pysmell_cls(self, cls):
        cls_name, info = cls
        cls_name = cls_name.replace(PYSMELL_PREFIX, '')
        args_constructor = info.get('constructor', None)
        args_constructor = ', '.join(args_constructor)
        args_constructor = ' (%s)' % args_constructor
        description = info.get('docstring', None)
        return self.createItemAutoComplete(cls_name,
                                           'class', args_constructor,
                                           description)

    def treatment_pysmell_into_cls(self, cls, resultList):
        for m in cls['methods']:
            item = self.treatment_pysmell_func(m)
            if not item in resultList:
                resultList.append(item)
        for m in cls['constructor']:
            item = self.treatment_pysmell_func(m)
            if not item in resultList:
                resultList.append(item)
        for m in cls['properties']:
            item = self.treatment_pysmell_const(m)
            if not item in resultList:
                resultList.append(item)


def createSignalAutocompleteDocument(view, *args, **kwargs):
    # https://launchpad.net/ubuntu/precise/+source/pykde4
    # https://launchpad.net/ubuntu/precise/+source/pykde4/4:4.7.97-0ubuntu1/+files/pykde4_4.7.97.orig.tar.bz2
    #http://doc.trolltech.com/4.6/qabstractitemmodel.html
    #http://gitorious.org/kate/kate/blobs/a17eb928f8133528a6194b7e788ab7a425ef5eea/ktexteditor/codecompletionmodel.cpp
    #http://code.google.com/p/lilykde/source/browse/trunk/frescobaldi/python/frescobaldi_app/mainapp.py#1391
    #http://api.kde.org/4.0-api/kdelibs-apidocs/kate/html/katecompletionmodel_8cpp_source.html
    #https://svn.reviewboard.kde.org/r/1640/diff/?expand=1
    PythonCodeCompletionModel.getPythonPath()
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(codecompletationmodel)

windowInterface = kate.application.activeMainWindow()
codecompletationmodel = PythonCodeCompletionModel(windowInterface)
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalAutocompleteDocument)
