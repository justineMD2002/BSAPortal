from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .form import *
from CreateAccount.models import User, Resident
from .models import Appointment, HealthCenter
from django.shortcuts import render
from .models import HealthCenter


Resident = apps.get_model('CreateAccount','Resident')
HealthCenter = apps.get_model('BookAppointment','HealthCenter')


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
    global username
    def get(self, request):
        login_form = LoginForm()
        return render(request, self.template_name, {'form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = Resident.objects.get(username=username, password=password, user_type="R")
                request.session['type'] = "R"
                request.session['user_id'] = user.user_id
                return redirect(reverse('bookappointment:book'))
            except Resident.DoesNotExist:
                messages.error(request, 'Invalid login credentials. Please try again.')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

        return render(request, 'login.html', {'form': login_form})


class BookAppointmentView(View):
    def post(self,request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.instance.healthCenter = HealthCenter.objects.first()
            form.save()
            return render(request, 'success.html')
        return render(request, 'bookappointment.html', {'form': form})
    def get(self,request):
        health_center = HealthCenter.objects.first()
        form = AppointmentForm(initial={'resident': request.session['user_id'], 'healthCenter': health_center.pk})
        return render(request, 'bookappointment.html', {'form': form})

