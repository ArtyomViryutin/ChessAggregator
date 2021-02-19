from django.core import validators
from django.db import models

from users.models import User


class Tournament(models.Model):

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    participants = models.ManyToManyField(User, related_name='tournaments', blank=True, through='Participation')
    name = models.CharField(max_length=120, unique=True)

    url = models.URLField(validators=[validators.URLValidator])

    location = models.CharField(max_length=120)
    open_date = models.DateField()
    close_date = models.DateField()

    fee = models.IntegerField(validators=[validators.MinValueValidator(0)])
    increment = models.IntegerField(validators=[validators.MinValueValidator(0)])
    prize_fund = models.IntegerField(validators=[validators.MinValueValidator(0)])
    minutes = models.IntegerField(validators=[validators.MinValueValidator(0)])
    seconds = models.IntegerField(validators=[validators.MinValueValidator(0)])
    tours = models.IntegerField(validators=[validators.MinValueValidator(0)])

    CURRENT = 'current'
    FORTHCOMING = 'forthcoming'
    COMPLETED = 'completed'
    STATUS_OPTIONS = (
        (CURRENT, 'current'),
        (FORTHCOMING, 'forthcoming'),
        (COMPLETED, 'completed')
    )
    status = models.CharField(max_length=11, choices=STATUS_OPTIONS, default=FORTHCOMING)

    CLASSIC = 'Классика'
    RAPID = 'Рапид'
    BLITZ = 'Блиц'
    BULLET = 'Пуля'
    FIDE_CLASSIC = 'Классика FIDE'
    CHESS960 = 'Шахматы 960'
    RATING_OPTIONS = (
        (CLASSIC, 'Классика'),
        (RAPID, 'Рапид'),
        (BLITZ, 'Блиц'),
        (BULLET, 'Пуля'),
        (FIDE_CLASSIC, 'Классика FIDE'),
        (CHESS960, 'Шахматы 960'),
    )
    mode = models.CharField(max_length=13, choices=RATING_OPTIONS, default=CLASSIC)

    FIDE = 'FIDE'
    FRC = 'ФШР'
    WITHOUT = 'Без обсчёта'
    MODE_OPTIONS = (
        (FIDE, 'FIDE'),
        (FRC, 'ФШР'),
        (WITHOUT, 'Без обсчёта')
    )
    rating_type = models.CharField(max_length=11, choices=MODE_OPTIONS, default=WITHOUT)


class ParticipationOptionChoices(models.TextChoices):
    WAITING = 'waiting'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'


class Participation(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    status = models.CharField(max_length=8, choices=ParticipationOptionChoices.choices,
                              default=ParticipationOptionChoices.WAITING)

    class Meta:
        unique_together = ('player', 'tournament')


class AnonymousParticipation(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=30, blank=False, null=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='anonymous_participants')

    status = models.CharField(max_length=8, choices=ParticipationOptionChoices.choices,
                              default=ParticipationOptionChoices.WAITING)
