# Generated by Django 4.2.1 on 2023-08-09 17:52

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_fewnu_compta', '0009_employee_createdby'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('numWhtsapp', models.CharField(blank=True, max_length=120, null=True)),
                ('pays', models.CharField(blank=True, max_length=120, null=True)),
                ('ville', models.CharField(blank=True, max_length=120, null=True)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True), blank=True, size=None)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]