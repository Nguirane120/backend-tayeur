# Generated by Django 4.1 on 2022-09-05 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_fewnu_compta', '0008_vente_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vente',
            name='status',
            field=models.CharField(choices=[('ENCOURS', 'ENCOURS'), ('ENVOYE', 'ENVOYE'), ('PAYE', 'PAYE'), ('ANNULE', 'ANNULE')], default='ENCOURS', max_length=10),
        ),
    ]
