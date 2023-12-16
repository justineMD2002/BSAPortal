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
from django.db import connection


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
            password = request.POST['password']
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            bdate = request.POST['birth_date']
            address = request.POST['present_address']
            result = ""
            cursor = connection.cursor()
            args = [username, password, fname, lname, bdate, address, result]
            cursor.callproc('reg_user', args)
            result1 = cursor.fetchall()
            msg = result1[0][0]
            cursor.close()

            if username + "Username exists" == msg:
                messages.error(request, 'User exists.')
                return render(request, 'registration.html', {'form': resident_form})
            else:
                return redirect(reverse('bookappointment:login'))
        else:
             messages.error(request, 'Registration invalid. Please try again.')

        return render(request, 'registration.html', {'form': resident_form})

        # previous implementation:
        # if resident_form.is_valid():
        #     username = request.POST['username']
        #     try:
        #         Resident.objects.get(username=username)
        #         messages.error(request, 'User exists.')
        #     except Resident.DoesNotExist:
        #         resident_form.save()
        #         return redirect(reverse('bookappointment:login'))
        # else:
        #     messages.error(request, 'Registration invalid. Please try again.')
        # return render(request, 'registration.html', {'form': resident_form})


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

            cursor = connection.cursor()
            args = [username, password]
            cursor.callproc('check_credentials', args)
            uid = cursor.fetchone()[0]

            if uid != 0:
                request.session['type'] = "R"
                request.session['user_id'] = uid
                return redirect(reverse('bookappointment:appointment_list'))
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

        return render(request, 'login.html', {'form': login_form})

        # previous implementation:
        #  login_form = LoginForm(request.POST)
        # if login_form.is_valid():
        #     username = login_form.cleaned_data.get('username')
        #     password = login_form.cleaned_data.get('password')
        #
        #     try:
        #         user = Resident.objects.get(username=username, password=password, user_type="R")
        #         request.session['type'] = "R"
        #         request.session['user_id'] = user.user_id
        #         return redirect(reverse('bookappointment:appointment_list'))
        #     except Resident.DoesNotExist:
        #         messages.error(request, 'Invalid login credentials. Please try again.')
        # else:
        #     messages.error(request, 'Invalid login credentials. Please try again.')
        #
        # return render(request, 'login.html', {'form': login_form})


class BookAppointmentView(View):
    def post(self,request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            user_id = request.session['user_id']
            type = request.POST['typeOfAppointment']
            date = request.POST['dateOfAppointment']
            time = request.POST['timeOfAppointment']
            result = ""
            cursor = connection.cursor()
            args = [date, time, 1, user_id, type, result]
            cursor.callproc('book_appointment', args)
            result2 = cursor.fetchall()
            msg = result2[0][0]
            cursor.close()

            if msg == 0:
                messages.error(request, 'Schedule is already reserved, please book again.')
                return render(request, 'bookappointment.html', {'form': form})
            else:
                return render(request, 'success.html')
        else:
            messages.error(request, 'Booking invalid. Please try again.')

        return render(request, 'bookappointment.html', {'form': form})

        # previous implementation
            # form.save()
        #   return render(request, 'success.html')
        # return render(request, 'bookappointment.html', {'form': form})
    def get(self,request):
        health_center = HealthCenter.objects.first()
        form = AppointmentForm(initial={'resident': request.session['user_id'], 'healthCenter': health_center.pk})
        return render(request, 'bookappointment.html', {'form': form})


def appointment_list(request):
    cursor = connection.cursor()
    query = "SELECT * FROM appointment"
    cursor.execute(query)
    appointments = cursor.fetchall()
    cursor.close()
    return render(request, 'appointment_list.html', {'appointments': appointments})

    # previous implementation:
    # appointments = Appointment.objects.all()
    # return render(request, 'appointment_list.html', {'appointments': appointments})


def myappointment_list(request):
    cursor = connection.cursor()
    user_id = request.session['user_id']
    query = "SELECT * FROM appointment WHERE resident_id = %s"
    cursor.execute(query, (user_id,))
    appointments = cursor.fetchall()
    cursor.close()
    return render(request, 'myappointment_list.html', {'appointments': appointments})

    # previous implementation:
    # user_id = request.session['user_id']
    # resident = Resident.objects.get(user_id=user_id)
    # appointments = Appointment.objects.filter(resident=resident)
    # return render(request, 'myappointment_list.html', {'appointments': appointments})