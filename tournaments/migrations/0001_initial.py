# Generated by Django 3.1.6 on 2021-02-23 16:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='waiting', max_length=8)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('url', models.URLField(validators=[django.core.validators.URLValidator])),
                ('location', models.CharField(max_length=120)),
                ('open_date', models.DateField()),
                ('close_date', models.DateField()),
                ('fee', models.IntegerField()),
                ('increment', models.IntegerField()),
                ('prize_fund', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('seconds', models.IntegerField()),
                ('tours', models.IntegerField()),
                ('status', models.CharField(choices=[('current', 'Current'), ('forthcoming', 'Forthcoming'), ('completed', 'Completed')], default='forthcoming', max_length=11)),
                ('mode', models.CharField(choices=[('Классика', 'Classic'), ('Рапид', 'Rapid'), ('Блиц', 'Blitz'), ('Пуля', 'Bullet'), ('Классика FIDE', 'Fide Classic'), ('Шахматы 960', 'Chess960')], default='Классика', max_length=13)),
                ('rating_type', models.CharField(choices=[('FIDE', 'Fide'), ('ФШР', 'Frc'), ('Без обсчёта', 'Without')], default='Без обсчёта', max_length=11)),
                ('organizer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(blank=True, related_name='tournaments', through='tournaments.Participation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='participation',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament'),
        ),
        migrations.CreateModel(
            name='AnonymousParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=40, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('birthdate', models.DateField()),
                ('patronymic', models.CharField(blank=True, max_length=30, null=True)),
                ('latin_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Latin name')),
                ('sex', models.CharField(choices=[('Мужчина', 'Man'), ('Женщина', 'Woman')], default='Мужчина', max_length=7)),
                ('fide_id', models.IntegerField(blank=True, null=True, verbose_name='FIDE ID')),
                ('frc_id', models.IntegerField(blank=True, null=True, verbose_name='FRC ID')),
                ('classic_fide_rating', models.IntegerField(blank=True, null=True, verbose_name='Classic')),
                ('rapid_fide_rating', models.IntegerField(blank=True, null=True, verbose_name='Rapid')),
                ('blitz_fide_rating', models.IntegerField(blank=True, null=True, verbose_name='Blitz')),
                ('classic_frc_rating', models.IntegerField(blank=True, null=True, verbose_name='Classic')),
                ('rapid_frc_rating', models.IntegerField(blank=True, null=True, verbose_name='Rapid')),
                ('blitz_frc_rating', models.IntegerField(blank=True, null=True, verbose_name='Blitz')),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='waiting', max_length=8)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anonymous_participants', to='tournaments.tournament')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together={('player', 'tournament')},
        ),
    ]
