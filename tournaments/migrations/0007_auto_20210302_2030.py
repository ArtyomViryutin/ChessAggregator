# Generated by Django 3.1.6 on 2021-03-02 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0006_auto_20210302_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='mode',
            field=models.CharField(choices=[('Классика', 'Classic'), ('Рапид', 'Rapid'), ('Блиц', 'Blitz'), ('Пуля', 'Bullet'), ('Классика FIDE', 'Fide Classic'), ('Шахматы 960', 'Chess960')], default='Классика', max_length=13),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='rating_type',
            field=models.CharField(choices=[('FIDE', 'Fide'), ('ФШР', 'Frc'), ('Без обсчёта', 'Without')], default='Без обсчёта', max_length=11),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='status',
            field=models.CharField(choices=[('current', 'Current'), ('forthcoming', 'Forthcoming'), ('completed', 'Completed')], default='forthcoming', max_length=11),
        ),
    ]
