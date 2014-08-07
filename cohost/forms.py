#encoding=utf-8
from django import forms

from cohost.models import STATE_CHOICES
from cohost.models import Cate

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DataStateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DataStateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-datastateForm'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
    state = forms.TypedChoiceField(
        label = u"审核状态",
        choices = STATE_CHOICES,
        widget = forms.Select,
        initial = '0',
        required = False,
    )
    cate = forms.ModelChoiceField(
        label = u"类别",
        queryset=Cate.objects.all(),
        widget = forms.Select,
        initial = '0',
        required = False,
    )


# class DataFilterForm(forms.Form):
#     """网站类型、有无备案、站点状态、接入商、审核状态"""

#     def __init__(self, *args, **kwargs):
#         super(DataFilterForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-datafilterForm'
#         self.helper.form_class = 'form, form-inline'
#         self.helper.form_method = 'get'
#         self.helper.add_input(Submit('submit', 'Submit'))
#     beian = forms.ChoiceField(
#         label = u"备案",
#         choices = ((True, u"有" ), (False, u"无")),
#         widget = forms.RadioSelect,
#         initial = '0',
#         required = False,
#     )
    