# Generated by Django 3.1.6 on 2021-02-15 18:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=40, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('birthdate', models.DateField()),
                ('is_organizer', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('patronymic_name', models.CharField(blank=True, max_length=30, null=True)),
                ('latin_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Latin name')),
                ('sex', models.CharField(choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Женщина')], max_length=7)),
                ('fide_id', models.IntegerField(blank=True, null=True, verbose_name='FIDE ID')),
                ('frc_id', models.IntegerField(blank=True, null=True, verbose_name='FRC ID')),
                ('classic_fide_rating', models.IntegerField(blank=True, null=True, verbose_name='Classic')),
                ('rapid_fide_rating', models.IntegerField(blank=True, null=True, verbose_name='Rapid')),
                ('blitz_fide_rating', models.IntegerField(blank=True, null=True, verbose_name='Blitz')),
                ('classic_frc_rating', models.IntegerField(blank=True, null=True, verbose_name='Classic')),
                ('rapid_frc_rating', models.IntegerField(blank=True, null=True, verbose_name='Rapid')),
                ('blitz_frc_rating', models.IntegerField(blank=True, null=True, verbose_name='Blitz')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
