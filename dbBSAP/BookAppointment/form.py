from django import forms
from CreateAccount.models import Resident


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class ResidentRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)
    first_name = forms.CharField(widget=forms.TextInput, max_length=30)
    last_name = forms.CharField(widget=forms.TextInput, max_length=30)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    present_address = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Resident
        fields = ['username', 'password', 'first_name', 'last_name', 'birth_date', 'present_address']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

