# Generated by Django 4.1 on 2022-08-26 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_fewnu_compta', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='qte',
        ),
    ]
