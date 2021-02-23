from django.core import validators
from django.db import models

from users.models import User, SexChoices


class Tournament(models.Model):

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    participants = models.ManyToManyField(User, related_name='tournaments', blank=True, through='Participation')
    name = models.CharField(max_length=120, unique=True)
    url = models.URLField(validators=[validators.URLValidator])
    location = models.CharField(max_length=120)
    open_date = models.DateField()
    close_date = models.DateField()
    fee = models.IntegerField()
    increment = models.IntegerField()
    prize_fund = models.IntegerField()
    minutes = models.IntegerField()
    seconds = models.IntegerField()
    tours = models.IntegerField()

    class TournamentStatusChoices(models.Choices):
        CURRENT = 'current'
        FORTHCOMING = 'forthcoming'
        COMPLETED = 'completed'
    status = models.CharField(max_length=11, choices=TournamentStatusChoices.choices,
                              default=TournamentStatusChoices.FORTHCOMING)

    class ModeChoices(models.Choices):
        CLASSIC = 'Классика'
        RAPID = 'Рапид'
        BLITZ = 'Блиц'
        BULLET = 'Пуля'
        FIDE_CLASSIC = 'Классика FIDE'
        CHESS960 = 'Шахматы 960'

    class RatingTypeChoices(models.Choices):
        FIDE = 'FIDE'
        FRC = 'ФШР'
        WITHOUT = 'Без обсчёта'

    mode = models.CharField(max_length=13, choices=ModeChoices.choices, default=ModeChoices.CLASSIC)
    rating_type = models.CharField(max_length=11, choices=RatingTypeChoices.choices, default=
                                   RatingTypeChoices.WITHOUT)


class ParticipationChoices(models.TextChoices):
    WAITING = 'waiting'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'


class Participation(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    status = models.CharField(max_length=8, choices=ParticipationChoices.choices,
                              default=ParticipationChoices.WAITING)

    class Meta:
        unique_together = ('player', 'tournament')


class AnonymousParticipation(models.Model):
    email = models.EmailField(validators=[validators.validate_email],
                              max_length=40, unique=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=30, blank=False, null=False)
    birthdate = models.DateField(blank=False, null=False)

    patronymic = models.CharField(max_length=30, blank=True, null=True)
    latin_name = models.CharField(max_length=60, blank=True, null=True, verbose_name='Latin name')

    sex = models.CharField(max_length=7, choices=SexChoices.choices, default=SexChoices.MAN)
    fide_id = models.IntegerField(blank=True, null=True, verbose_name='FIDE ID')
    frc_id = models.IntegerField(blank=True, null=True, verbose_name='FRC ID')
    classic_fide_rating = models.IntegerField(blank=True, null=True, verbose_name='Classic')
    rapid_fide_rating = models.IntegerField(blank=True, null=True, verbose_name='Rapid')
    blitz_fide_rating = models.IntegerField(blank=True, null=True, verbose_name='Blitz')
    classic_frc_rating = models.IntegerField(blank=True, null=True, verbose_name='Classic')
    rapid_frc_rating = models.IntegerField(blank=True, null=True, verbose_name='Rapid')
    blitz_frc_rating = models.IntegerField(blank=True, null=True, verbose_name='Blitz')

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='anonymous_participants')
    status = models.CharField(max_length=8, choices=ParticipationChoices.choices,
                              default=ParticipationChoices.WAITING)


