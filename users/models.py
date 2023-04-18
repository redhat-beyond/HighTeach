from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Profile(models.Model):
    class Account_type(models.TextChoices):
        TEACHER = 'T', _('Teacher')
        STUDENT = 'S', _('Student')
        BOTH = 'B', _('Teacher and Student')

    class Meeting_method (models.TextChoices):
        LIVE = 'L', _('Live')
        ONLINE = 'O', _('Online')
        BOTH = 'B', _('Live and Online')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profession = models.TextField(max_length=100, blank=True, validators=[MaxLengthValidator(100)])
    phone_regex = RegexValidator(regex=r'^\+?0?\d{9,15}$',
                                 message="Phone number must be entered in the format:"
                                 + "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    city = models.CharField(max_length=30)
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

    def __str__(self):
        return f"{self.user.username}'s Profile"
