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
