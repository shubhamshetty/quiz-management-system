from django import forms
from QMS.models import Questionnaire

class Questionnaireforms(forms.ModelForm):
    class Meta:
        model = Questionnaire
        exclude = ['quiz', 'category']
