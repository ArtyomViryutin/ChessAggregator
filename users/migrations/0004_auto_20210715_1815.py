# Generated by Django 3.1.6 on 2021-07-15 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210302_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('Мужчина', 'Man'), ('Женщина', 'Woman')], default='Мужчина', max_length=7),
        ),
    ]
