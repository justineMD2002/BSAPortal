# Generated by Django 4.2.6 on 2023-12-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreateAccount', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='user_type',
            field=models.CharField(choices=[('R', 'Resident'), ('O', 'Organization'), ('A', 'Admin')], default='R', max_length=1),
        ),
        migrations.AlterField(
            model_name='organization',
            name='user_type',
            field=models.CharField(choices=[('R', 'Resident'), ('O', 'Organization'), ('A', 'Admin')], default='R', max_length=1),
        ),
        migrations.AlterField(
            model_name='resident',
            name='user_type',
            field=models.CharField(choices=[('R', 'Resident'), ('O', 'Organization'), ('A', 'Admin')], default='R', max_length=1),
        ),
    ]
