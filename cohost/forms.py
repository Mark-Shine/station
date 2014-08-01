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