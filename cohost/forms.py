from django import forms

from cohost.models import STATE_CHOICES

from crispy_forms.layout import Submit

class DataStateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DataStateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-datastateForm'
        self.helper.form_class = 'forms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'change_host_state'

        self.helper.add_input(Submit('submit', 'Submit'))


    state = forms.TypedChoiceField(
        label = u"域名状态",
        choices = STATE_CHOICES,
        widget = forms.RadioSelect,
        initial = '0',
        required = True,
    )
