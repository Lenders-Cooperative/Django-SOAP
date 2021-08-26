# Generated by Django 3.2.6 on 2021-08-07 06:21

from django.db import migrations, models
import django_soap.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_soap', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='soaprequestlogger',
            options={'ordering': ('-date_sent',)},
        ),
        migrations.AlterModelOptions(
            name='soapresponselogger',
            options={'ordering': ('-date_received',)},
        ),
        migrations.AlterField(
            model_name='soaprequestlogger',
            name='method',
            field=models.CharField(choices=[('POST', 'POST'), ('GET', 'GET')], default=django_soap.models.VERBMAP['POST'], max_length=4),
        ),
    ]
