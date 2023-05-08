# from random import choice
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
# from django.core.exceptions import ValidationError
from django.db.models import Q


class Account_type(models.TextChoices):
    TEACHER = 'T', _('Teacher')
    STUDENT = 'S', _('Student')
    BOTH = 'B', _('Teacher and Student')


class Meeting_method (models.TextChoices):
    LIVE = 'L', _('Live')
    ONLINE = 'O', _('Online')
    BOTH = 'B', _('Live and Online')


class Profile(models.Model):
    # profile_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, max_length=500)
    profession = models.TextField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    phone_regex = RegexValidator(regex=r'^\+?0?\d{9,15}$',
                                 message="Phone number must be entered in the format:"
                                 + "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    account_type = models.CharField(
        max_length=1,
        choices=Account_type.choices,
        default=Account_type.STUDENT,
        )
    meeting_method = models.CharField(
        max_length=1,
        choices=Meeting_method.choices,
        default=Meeting_method.BOTH,
        )

    @staticmethod
    def create(username, password, account_type, first_name, last_name, meeting_method=Meeting_method.BOTH,
               email=None, phone_number=None, city=None, bio=None, profession=None):

        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name, email=email)
        profile = Profile.objects.create(user=user, phone_number=phone_number, city=city, account_type=account_type,
                                         meeting_method=meeting_method, bio=bio, profession=profession)

        return profile

    def save(self, *args, **kwargs):
        self.full_clean()
        self.user.save()
        return super().save(*args, **kwargs)

    @staticmethod
    def __str__(self):
        return f"{self.user.username}'s Profile"

    @staticmethod
    def filter_by_account_type(account_type):
        return Profile.objects.filter(account_type=account_type) if account_type else []

    @staticmethod
    def filter_by_city(city):

        return Profile.objects.filter(city=city) if city else []

    @staticmethod
    def filter_by_first_name(first_name):
        users_ids = User.objects.filter(first_name=first_name).values('id') if first_name else []

        return Profile.objects.filter(Q(user_id__in=users_ids)) if users_ids else []

    @staticmethod
    def filter_by_last_name(last_name):
        users_ids = User.objects.filter(last_name=last_name).values('id') if last_name else []

        return Profile.objects.filter(Q(user_id__in=users_ids)) if users_ids else []
