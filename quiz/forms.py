from django import forms
from django.forms.widgets import RadioSelect

CHOICES = (
    ('US', 'United States'),
    ('FR', 'France'),
    ('CN', 'China'),
    ('RU', 'Russia'),
    ('IT', 'Italy'),
)

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)


class TypeForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

    favorite_fruit = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=CHOICES))