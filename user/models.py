from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class MyUserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not first_name:
            raise ValueError("Users must have an first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not phone_number:
            raise ValueError("Users must have an phone number")

        user = self.model(
                email=self.normalize_email(email),
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, phone_number, password):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Account_type(models.TextChoices):
        TEACHER = 'T', _('Teacher')
        STUDENT = 'S', _('Student')
        BOTH = 'B', _('Teacher and Student')

    class Meeting_method (models.TextChoices):
        LIVE = 'L', _('Live')
        ONLINE = 'O', _('Online')
        BOTH = 'B', _('Live and Online')

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number',]
    objects = MyUserManager()

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
