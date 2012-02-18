from PyKDE4.kdeui import KIcon
from PyKDE4.ktexteditor import KTextEditor
from PyQt4.QtCore import QModelIndex, QSize, Qt, QVariant


class AbstractCodeCompletionModel(KTextEditor.CodeCompletionModel):

    MIMETYPES = None

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

    def completionInvoked(self, view, word, invocationType):
        is_auto = False
        line_start = word.start().line()
        line_end = word.end().line()
        self.resultList = []
        self.invocationType = invocationType
        path = unicode(view.document().url().path())
        if line_start != line_end:
            return
        if not path.split(".")[-1] in self.MIMETYPES:
            return
        doc = view.document()
        line = unicode(doc.line(line_start))
        if not line:
            return
        return (is_auto, self.parse_line(line))

    def data(self, index, role, *args, **kwargs):
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

    #http://api.kde.org/4.5-api/kdelibs-apidocs/interfaces/ktexteditor/html/classKTextEditor_1_1CodeCompletionModel.html#3bd60270a94fe2001891651b5332d42b
    def index(self, row, column, parent):
        if (row < 0 or row >= len(self.resultList) or
            column < 0 or column >= KTextEditor.CodeCompletionModel.ColumnCount or
            parent.isValid()):
            return QModelIndex()
        return self.createIndex(row, column)

    def parse_line(self, line):
        return line

    def rowCount(self, parent):
        if parent.isValid():
            return 0  # Do not make the model look hierarchical
        else:
            return len(self.resultList)
