from django import forms
from django.contrib.auth.models import User

from stacquora.models import Question, Answer, QuestionComment

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('username', 'first_name', 'email')

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Different passwords in the fields')
        return cd['password2']

class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description']

class AnswerQuestion(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']
