# Generated by Django 3.1.6 on 2021-02-15 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='patronymic_name',
            new_name='patronymic',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='surname',
        ),
    ]
