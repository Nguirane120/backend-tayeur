# Generated by Django 4.1.1 on 2023-04-16 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_fewnu_compta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
