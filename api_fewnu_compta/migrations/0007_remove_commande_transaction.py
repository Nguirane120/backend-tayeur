# Generated by Django 4.2.1 on 2023-06-12 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_fewnu_compta", "0006_commande_transaction_alter_transaction_commande"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="commande",
            name="transaction",
        ),
    ]
