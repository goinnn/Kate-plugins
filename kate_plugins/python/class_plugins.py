import wx 
import kate

from utils import insertText


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
    app = wx.PySimpleApp()
    frame = MyFrame(currentDocument=currentDocument, view=view,
                    pattern_str=pattern_str, title=title,
                    name_field=name_field)
    frame.Show(True)
    app.MainLoop()


class MyFrame(wx.Frame):

    def __init__(self, currentDocument, view, pattern_str='', title='', name_field=''):
        wx.Frame.__init__(self, None, -1, title, size=(300, 60))
        panel = wx.Panel(self, -1)

        wx.StaticText(panel, -1, name_field, pos=(10, 10), size=(150, 25))
        self.posCtrl = wx.TextCtrl(panel, -1, "", pos=(100, 10))
        button = wx.Button(panel, label='Ok', pos=(200, 10),
                size=(50, 25))
        self.Bind(wx.EVT_BUTTON, self.OnPressButton, button)
        self.currentDocument = currentDocument
        self.view = view
        self.pattern_str = pattern_str

    def OnPressButton(self, event):
        class_name = self.posCtrl.GetValue()
        class_model = class_name.replace('Form', '')
        text = self.pattern_str % {'class_name': class_name, 'class_model':class_model}
        self.currentDocument.insertText(self.view.cursorPosition(), text)
        self.Close(True)


@kate.action('Create form', shortcut='Ctrl+Alt+F', menu='Edit')
def create_form():
    create_frame(pattern_str=PATTERN_MODEL_FORM, title='Create Form',
                 name_field='Name Form')


@kate.action("Create model", shortcut="Ctrl+Alt+M", menu='Edit')
def create_model():
    create_frame(pattern_str=PATTERN_MODEL, title='Create Model',
                 name_field='Name Model')

