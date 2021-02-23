from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, AbstractUser)
from django.core import validators
from django.db import models, transaction


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email=email, password=password, **extra_fields)


class SexChoices(models.Choices):
    MAN = 'Мужчина'
    WOMAN = 'Женщина'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(validators=[validators.validate_email],
                              max_length=40, unique=True, blank=False)
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
    is_organizer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name', 'surname', 'patronymic', 'sex', 'birthdate', 'latin_name', 'fide_id', 'frc_id',
    #                    'is_organizer', 'fide_id', 'frc_id', 'classic_fide_rating', 'rapid_fide_rating',
    #                    'blitz_fide_rating', 'classic_frc_rating', 'rapid_frc_rating', 'blitz_frc_rating', 'latin_name']
    REQUIRED_FIELDS = ['birthdate']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
