from django import forms
from CreateAccount.models import User, Resident
from .models import Appointment, HealthCenter
from django.http import request
from django.apps import apps


Resident = apps.get_model('CreateAccount', 'Resident')


class ResidentRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, max_length=15, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, max_length=20, label='Password')
    first_name = forms.CharField(widget=forms.TextInput, max_length=30, label='Firstname')
    last_name = forms.CharField(widget=forms.TextInput, max_length=30, label='Lastname')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Birthdate')
    present_address = forms.CharField(widget=forms.TextInput, label='Present Address')
    user_type = forms.CharField(widget=forms.HiddenInput, initial='R')

    class Meta:
        model = Resident
        fields = ['username', 'password', 'first_name', 'last_name', 'birth_date', 'present_address', 'user_type']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class AppointmentForm(forms.ModelForm):
    typeOfAppointment = forms.ChoiceField(choices=Appointment.appointment_choices,
                                          widget=forms.Select, label='Type of Appointment')
    dateOfAppointment = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                        label='Date of Appointment')
    timeOfAppointment = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}),
                                        label='Time of Appointment')
    appointment_status = forms.CharField(widget=forms.HiddenInput, initial='P')
    resident = forms.ModelChoiceField(
        queryset=Resident.objects.all(),
        widget=forms.HiddenInput,
    )
    healthCenter = forms.ModelChoiceField(
        queryset=HealthCenter.objects.all(),
        widget=forms.HiddenInput,
    )
    class Meta:
        model = Appointment
        fields = ['typeOfAppointment', 'dateOfAppointment', 'timeOfAppointment', 'appointment_status', 'resident']
