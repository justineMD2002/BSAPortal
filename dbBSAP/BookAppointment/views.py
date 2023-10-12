from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .form import *
from CreateAccount.models import Resident


def index(request):
    return HttpResponse("hello world")


def DefaultView(request):
    return redirect(reverse('bookappointment:login'))


class RegistrationView(View):
    template_name = 'registration.html'

    def get(self, request):
        resident_form = ResidentRegistrationForm()
        return render(request, self.template_name, {'form': resident_form})

    def post(self, request):
        resident_form = ResidentRegistrationForm(request.POST)
        if resident_form.is_valid():
            username = request.POST['username']
            try:
                Resident.objects.get(username=username)
                messages.error(request, 'User exists.')
            except Resident.DoesNotExist:
                resident_form.save()
                return redirect(reverse('bookappointment:login'))
        else:
            messages.error(request, 'Registration invalid. Please try again.')
        return render(request, 'registration.html', {'form': resident_form})


class Login(View):
    template_name = 'login.html'

    def get(self, request):
        login_form = LoginForm()
        return render(request, self.template_name, {'form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            try:
                Resident.objects.get(username=username, password=password)
                return render(request, 'success.html')
            except Resident.DoesNotExist:
                messages.error(request, 'Invalid login credentials. Please try again.')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

        return render(request, 'login.html', {'form': login_form})
