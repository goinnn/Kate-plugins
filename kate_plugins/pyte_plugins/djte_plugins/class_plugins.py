import kate

from PyQt4 import QtGui
from kate_settings_plugins import KATE_ACTIONS


PATTERN_MODEL_FORM = """

class %(class_name)s(forms.ModelForm):

    class Meta:
        model = %(class_model)s

    def __init__(self, *args, **kwargs):
        super(%(class_name)s, self).__init__(*args, **kwargs)

    def clean(self):
        return super(%(class_name)s, self).clean()

    def save(self, commit=True):
        return super(%(class_name)s, self).save(commit)

"""

PATTERN_MODEL = """

class %(class_name)s(models.Model):

    class Meta:
        verbose_name = _('%(class_name)s')
        verbose_name_plural = _('%(class_name)ss')

    @permalink
    def get_absolute_url(self):
        pass

    def __unicode__(self):
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


@kate.action(**KATE_ACTIONS['createForm'])
def createForm():
    create_frame(pattern_str=PATTERN_MODEL_FORM, title='Create Form',
                 name_field='Name Form')


@kate.action(**KATE_ACTIONS['createModel'])
def createModel():
    create_frame(pattern_str=PATTERN_MODEL, title='Create Model',
                 name_field='Name Model')
