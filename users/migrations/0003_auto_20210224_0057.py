# Generated by Django 3.1.6 on 2021-02-23 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210224_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('Мужчина', 'Man'), ('Женщина', 'Woman')], default='Мужчина', max_length=7),
        ),
    ]