# Generated by Django 4.1.7 on 2023-03-26 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='date_joiners',
            new_name='date_joined',
        ),
    ]