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

    fee = models.IntegerField()
    increment = models.IntegerField()
    prize_fund = models.IntegerField()
    minutes = models.IntegerField()
    seconds = models.IntegerField()
    tours = models.IntegerField()

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
    email = models.EmailField(validators=[validators.validate_email],
                              max_length=40, unique=True, blank=False)
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=30, blank=False, null=False)
    birthdate = models.DateField(blank=False, null=False)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    latin_name = models.CharField(max_length=60, blank=True, null=True, verbose_name='Latin name')

    MAN = 'Мужчина'
    WOMAN = 'Женщина'
    SEX_OPTIONS = (
        (MAN, 'Мужчина'),
        (WOMAN, 'Женщина'))
    sex = models.CharField(max_length=7, blank=False, choices=SEX_OPTIONS)
    fide_id = models.IntegerField(blank=True, null=True, verbose_name='FIDE ID')
    frc_id = models.IntegerField(blank=True, null=True, verbose_name='FRC ID')
    classic_fide_rating = models.IntegerField(blank=True, null=True, verbose_name='Classic')
    rapid_fide_rating = models.IntegerField(blank=True, null=True, verbose_name='Rapid')
    blitz_fide_rating = models.IntegerField(blank=True, null=True, verbose_name='Blitz')
    classic_frc_rating = models.IntegerField(blank=True, null=True, verbose_name='Classic')
    rapid_frc_rating = models.IntegerField(blank=True, null=True, verbose_name='Rapid')
    blitz_frc_rating = models.IntegerField(blank=True, null=True, verbose_name='Blitz')

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='anonymous_participants')
    status = models.CharField(max_length=8, choices=ParticipationOptionChoices.choices,
                              default=ParticipationOptionChoices.WAITING)



