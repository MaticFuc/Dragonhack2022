from django import forms
from django.forms.widgets import RadioSelect

CHOICES = (
    ('WMC', 'Wikipedia - Multiple choice'),
    ('WFI', 'Wikipedia - Fill in'),
    ('TMC', 'Textbook - Multiple choice'),
    ('TFI', 'Textbook - Fill in'),
)

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)


class TypeForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

    
    
class AppForm(forms.Form):
    text_area = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':'10', 'cols':'20'}),required = False)
    WMC = forms.CharField(label="App type", widget=forms.Select(choices = CHOICES))
    query = forms.CharField(label="query", max_length = 100,required = False)
    class Meta:
        pass
        #self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)
        #fields = ["app_choice"]