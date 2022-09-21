# Generated by Django 4.1 on 2022-08-26 14:47

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(max_length=40)),
                ('firstName', models.CharField(blank=True, max_length=100)),
                ('lastName', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('tailleur', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_type', models.CharField(blank=True, choices=[('owner', 'owner'), ('manager', 'manager'), ('collaborator', 'collaborator'), ('tailleur', 'tailleur')], default='owner', max_length=20)),
                ('archived', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.IntegerField(default=1)),
                ('total', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'api_fewnu_compta_article',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=512)),
                ('archived', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_fewnu_compta_category',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('firstName', models.CharField(max_length=250)),
                ('lastName', models.CharField(max_length=250)),
                ('telephone', models.CharField(max_length=30)),
                ('adresse', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('archived', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_fewnu_compta_client',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('libelle', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=512)),
                ('qte', models.IntegerField()),
                ('min_stock', models.IntegerField()),
                ('prix_achat', models.IntegerField()),
                ('prix_vente', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('archived', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to='api_fewnu_compta.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_fewnu_compta_produit',
            },
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('archived', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_fewnu_compta.customer')),
                ('products', models.ManyToManyField(through='api_fewnu_compta.Article', to='api_fewnu_compta.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_fewnu_compta_vente',
            },
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('firstName', models.CharField(max_length=250)),
                ('lastName', models.CharField(max_length=250)),
                ('telephone', models.CharField(max_length=30)),
                ('adresse', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('archived', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fournisseur', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_fewnu_compta_fournisseur',
            },
        ),
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('product_list', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), default=None, size=None)),
                ('total', models.IntegerField(default=0)),
                ('archived', models.BooleanField(default=False)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fournisseur', to='api_fewnu_compta.fournisseur')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depense_by_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_fewnu_compta_depense',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_fewnu_compta.product'),
        ),
        migrations.AddField(
            model_name='article',
            name='vente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='api_fewnu_compta.vente'),
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('products', 'vente')},
        ),
    ]
