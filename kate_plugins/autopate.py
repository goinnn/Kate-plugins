from os import path
from simplejson import loads

from PyKDE4.kdeui import KIcon
from PyKDE4.ktexteditor import KTextEditor
from PyQt4.QtCore import QModelIndex, QSize, Qt, QVariant


class AbstractCodeCompletionModel(KTextEditor.CodeCompletionModel):

    MIMETYPES = None
    OPERATORS = []
    SEPARATOR = '.'

    def __init__(self, *args, **kwargs):
        super(AbstractCodeCompletionModel, self).__init__(*args, **kwargs)
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

    @classmethod
    def createItemAutoComplete(cls, text, icon='unknown', args=None,
                               description=None, place='code'):
        icon_converter = {'package': 'code-block',
                          'module': 'code-context',
                          'unknown': 'unknown',
                          'constant': 'code-variable',
                          'class': 'code-class',
                          'function': 'code-function'}
        max_description = 50
        if description and len(description) > max_description:
            description = description.strip()
            description = '%s...' % description[:max_description]
        return {'text': text,
                'icon': icon_converter[icon],
                'args': args or '',
                'type': icon,
                'description': description or ''}

    def completionInvoked(self, view, word, invocationType):
        line_start = word.start().line()
        line_end = word.end().line()
        self.resultList = []
        self.invocationType = invocationType
        document_path = unicode(view.document().url().path())
        if line_start != line_end:
            return None
        if not document_path.split(".")[-1] in self.MIMETYPES:
            return None
        doc = view.document()
        line = unicode(doc.line(line_start))
        if not line:
            return line
        return self.parse_line(line)

    def data(self, index, role, *args, **kwargs):
        #http://api.kde.org/4.5-api/kdelibs-apidocs/kate/html/katewordcompletion_8cpp_source.html
        item = self.resultList[index.row()]
        if index.column() == KTextEditor.CodeCompletionModel.Name:
            if role == Qt.DisplayRole:
                return QVariant(item['text'])
            try:
                return self.roles[role]
            except KeyError:
                pass
        elif index.column() == KTextEditor.CodeCompletionModel.Icon:
            if role == Qt.DecorationRole:
                return QVariant(KIcon(item["icon"]).pixmap(QSize(16, 16)))
        elif index.column() == KTextEditor.CodeCompletionModel.Arguments:
            item_args = item.get("args", None)
            if role == Qt.DisplayRole and item_args:
                return QVariant(item_args)
        elif index.column() == KTextEditor.CodeCompletionModel.Postfix:
            item_description = item.get("description", None)
            if role == Qt.DisplayRole and item_description:
                return QVariant(item_description)
        return QVariant()

    def executeCompletionItem(self, doc, word, row):
        return super(AbstractCodeCompletionModel, self).executeCompletionItem(doc, word, row)

    def get_expression_last_expression(self, line):
        opmax = max(self.OPERATORS, key=lambda e: line.rfind(e))
        opmax_index = line.rfind(opmax)
        if line.find(opmax) != -1:
            line = line[opmax_index + 1:]
        return line.strip()

    #http://api.kde.org/4.5-api/kdelibs-apidocs/interfaces/ktexteditor/html/classKTextEditor_1_1CodeCompletionModel.html#3bd60270a94fe2001891651b5332d42b
    def index(self, row, column, parent):
        if (row < 0 or row >= len(self.resultList) or
            column < 0 or column >= KTextEditor.CodeCompletionModel.ColumnCount or
            parent.isValid()):
            return QModelIndex()
        return self.createIndex(row, column)

    def parse_line(self, line):
        return line.strip()

    def rowCount(self, parent):
        if parent.isValid():
            return 0  # Do not make the model look hierarchical
        else:
            return len(self.resultList)


class AbstractJSONFileCodeCompletionModel(AbstractCodeCompletionModel):

    FILE_PATH = None

    def __init__(self, *args, **kwargs):
        super(AbstractJSONFileCodeCompletionModel, self).__init__(*args, **kwargs)
        abs_file_path = path.join(path.dirname(path.abspath(__file__)),
                                  self.FILE_PATH)
        json_str = open(abs_file_path).read()
        self.json = loads(json_str)

    def completionInvoked(self, view, word, invocationType):
        line = super(AbstractJSONFileCodeCompletionModel, self).completionInvoked(view, word, invocationType)
        line = self.get_expression_last_expression(line)
        children = self.get_children_in_json(line, self.json)
        for child, attrs in children.items():
            self.resultList.append(self.createItemAutoComplete(text=child,
                                                               icon=attrs.get('icon', 'unknown')))

    def get_children_in_json(self, keys, json):
        if not self.SEPARATOR in keys:
            return json
        keys_split = keys.split(self.SEPARATOR)
        if keys_split and keys_split[0] in json:
            keys = self.SEPARATOR.join(keys_split[1:])
            return self.get_children_in_json(keys, json[keys_split[0]].get('children', None))
        return None
