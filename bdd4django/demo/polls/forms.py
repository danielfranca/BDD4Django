# *-* coding: utf-8 *-*

from django import forms
from django.utils.translation import ugettext_lazy as _

from polls.models import PollChoice,Choice

class PollChoiceForm(forms.ModelForm):

    class Meta:
        model = PollChoice
        fields = ('choice',)

    def __init__(self, poll, *args, **kwargs):
        super(PollChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ModelChoiceField(queryset=Choice.objects.filter(poll=poll), label=_('Choice'), widget=forms.widgets.RadioSelect)

