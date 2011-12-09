import kate

from PyQt4 import QtGui


PATTERN_MODEL_FORM = """

class %(class_name)s(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(%(class_name)s, self).__init__(*args, **kwargs)

    def clean(self):
        return super(%(class_name)s, self).clean()

    def save(self, commit=True):
        return super(%(class_name)s, self).save(commit)

    class Meta:
        model = %(class_model)s

    """

PATTERN_MODEL = """

class %(class_name)s(models.Model):

    def __unicode__(self):
        pass

    @permalink
    def get_absolute_url(self):
        pass

    class Meta:
        pass

    """


def create_frame(pattern_str='', title='', name_field=''):
    currentDocument = kate.activeDocument()
    view = kate.activeView()
    class_name, ok = QtGui.QInputDialog.getText(view, title, name_field)
    if ok:
        class_name = unicode(class_name)
        class_model = class_name.replace('Form', '')
        text = pattern_str % {'class_name': class_name,
                              'class_model': class_model}
        currentDocument.insertText(view.cursorPosition(), text)


@kate.action('Create form', shortcut='Ctrl+Alt+F', menu='Edit')
def create_form():
    create_frame(pattern_str=PATTERN_MODEL_FORM, title='Create Form',
                 name_field='Name Form')


@kate.action("Create model", shortcut="Ctrl+Alt+M", menu='Edit')
def create_model():
    create_frame(pattern_str=PATTERN_MODEL, title='Create Model',
                 name_field='Name Model')
