# Generated by Django 4.2.6 on 2023-11-02 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookAppointment', '0005_alter_appointment_dateofapproval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointmentStatus',
            field=models.CharField(choices=[('P', 'Pending'), ('R', 'Rejected'), ('A', 'Approved')], default='P', max_length=1),
        ),
    ]
