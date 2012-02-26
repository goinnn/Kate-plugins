import sys

import kate

from PyKDE4.ktexteditor import KTextEditor
from PyQt4 import QtCore

from autopate import AbstractCodeCompletionModel
from pyte_plugins.autocomplete.pyplete import PyPlete
from pyte_plugins.autocomplete.parse import (from_first_imporable, import_complete,
                                             from_other_imporables, from_complete)

global python_path
global windowInterface
global codecompletationmodel
global pyplete
python_path = []

PYSMELL_PREFIX = '__package____imporable__.'


class PythonCodeCompletionModel(AbstractCodeCompletionModel):

    MIMETYPES = ['', 'py', 'pyc']
    OPERATORS = ["=", " ", "[", "]", "(", ")", "{", "}", ":", ">", "<",
                 "+", "-", "*", "/", "%", " and ", " or ", ","]

    @classmethod
    def getPythonPath(cls):
        global python_path
        if python_path:
            return python_path
        python_path = sys.path
        try:
            from pyte_plugins.autocomplete import autocomplete_path
            doc = kate.activeDocument()
            view = doc.activeView()
            python_path = autocomplete_path.path(doc, view) + python_path
            sys.path = python_path
        except ImportError:
            pass
        return python_path

    def completionInvoked(self, view, word, invocationType):
        line = super(PythonCodeCompletionModel, self).completionInvoked(view,
                                                       word, invocationType)
        if line is None:
            return
        is_auto = False
        line_rough = line
        if 'from' in line or 'import' in line:
            is_auto = self.autoCompleteImport(view, word, line)
        line = self.getLastExpression(line)
        if not is_auto and line:
            is_auto = self.autoCompleteLine(view, word, line)
        if not is_auto and line and line_rough and not self.SEPARATOR in line_rough:
            is_auto = self.autoCompleteFile(view, word, line)

    def executeCompletionItem(self, doc, word, row):
        raw, col = word.start().position()
        line = unicode(doc.line(raw))
        line = self.parseLine(line)
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

    def parseLine(self, line):
        line = super(PythonCodeCompletionModel, self).parseLine(line)
        if "'" in line or '"' in line:
            return line
        if ";" in line:
            return self.parseLine(line.split(";")[-1])
        return line

    def autoCompleteImport(self, view, word, line):
        mfb = from_first_imporable.match(line) or import_complete.match(line)
        if mfb:
            return pyplete.get_importables_top_level(self.resultList)
        mfom = from_other_imporables.match(line)
        if mfom:
            imporable, subimporables = mfom.groups()
            if not subimporables:
                subimporables = []
            else:
                subimporables = subimporables.split(self.SEPARATOR)[:-1]
            return pyplete.get_importables_rest_level(self.resultList, imporable,
                                                      subimporables, into_module=False)
        mfc = from_complete.match(line)
        if mfc:
            imporable, subimporables, import_imporable = mfc.groups()
            if subimporables:
                subimporables = subimporables.split(self.SEPARATOR)
            else:
                subimporables = []
            return pyplete.get_importables_rest_level(self.resultList, imporable,
                                                      subimporables, into_module=True)
        return False

    def autoCompleteLine(self, view, word, line):
        try:
            last_dot = line.rindex(self.SEPARATOR)
            line = line[:last_dot]
        except ValueError:
            pass
        text = self._parseText(view, word, line)
        return self.getImportablesFromLine(self.resultList, text, line)

    def autoCompleteFile(self, view, word, line):
        text = self._parseText(view, word, line)
        return self.getImportablesFromText(self.resultList, text)

    def getImportablesFromLine(self, list_autocomplete, text,
                               code_line, text_info=True):
        try:
            return pyplete.get_importables_from_line(list_autocomplete, text,
                                                     code_line, text_info)
        except SyntaxError, e:
            self.treatmentException(e)
        return False

    def getImportablesFromText(self, list_autocomplete, text, line=None):
        try:
            return pyplete.get_importables_from_text(list_autocomplete, text, line)
        except SyntaxError, e:
            self.treatmentException(e)
        return False

    def treatmentException(self, e):
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
        kate.gui.popup(message, 2, icon='dialog-warning', minTextWidth=200)

    def _parseText(self, view, word, line):
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


def createSignalAutocompleteDocument(view, *args, **kwargs):
    # https://launchpad.net/ubuntu/precise/+source/pykde4
    # https://launchpad.net/ubuntu/precise/+source/pykde4/4:4.7.97-0ubuntu1/+files/pykde4_4.7.97.orig.tar.bz2
    #http://doc.trolltech.com/4.6/qabstractitemmodel.html
    #http://gitorious.org/kate/kate/blobs/a17eb928f8133528a6194b7e788ab7a425ef5eea/ktexteditor/codecompletionmodel.cpp
    #http://code.google.com/p/lilykde/source/browse/trunk/frescobaldi/python/frescobaldi_app/mainapp.py#1391
    #http://api.kde.org/4.0-api/kdelibs-apidocs/kate/html/katecompletionmodel_8cpp_source.html
    #https://svn.reviewboard.kde.org/r/1640/diff/?expand=1
    global pyplete
    pyplete = PyPlete(PythonCodeCompletionModel.createItemAutoComplete,
                      PythonCodeCompletionModel.getPythonPath())
    cci = view.codeCompletionInterface()
    cci.registerCompletionModel(codecompletationmodel)

windowInterface = kate.application.activeMainWindow()
codecompletationmodel = PythonCodeCompletionModel(windowInterface)
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalAutocompleteDocument)
