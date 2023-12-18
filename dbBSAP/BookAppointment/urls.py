from . import views
from django.urls import path

app_name = 'bookappointment'

urlpatterns = [
    path('', views.DefaultView, name="default"),
    path('bookappointment/register/', views.RegistrationView.as_view(), name="register"),
    path('bookappointment/login/', views.Login.as_view(), name="login"),
    path('bookappointment/book/', views.BookAppointmentView.as_view(), name="book"),
    path('bookappointment/appointments/', views.appointment_list, name='appointment_list'),
    path('bookappointment/myappointments/', views.myappointment_list, name='myappointment_list'),
    path('bookappointment/logout/', views.logout_view, name='logout'),
]