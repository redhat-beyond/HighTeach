# from django.test import TestCase
import pytest
from users.models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone


CREATION_DATE = timezone.now()


USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
PHONE_NUMBER = "0541234567"
LONG_PROFESSION = " test test test test test test test test test test test test test test test test" \
                 " test test test test test test test test test" \
                 " test test test test test test test test" \
                 " test test test test "
LONG_BIO = """ test test test test test test test test test test test test test test test test
                test test test test test test test test test test test test test test test test
                test test test test test test test test test test test test test test test test
                test test test test test test test test test test test test test test test test"""\
                 """ test test test test test test test test test test test test test test test test
                   test test test test test test test test test""" \
                 " test test test test test test test test test" \
                 " test test test test "


@pytest.fixture
def new_user():
    user = User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, email=EMAIL)
    user.set_password(PASSWORD)
    return user


@pytest.fixture
def new_second_user():
    user = User(username='second_user', first_name='second', last_name='user', email='email@gmail.com')
    user.set_password('second_pass')
    return user


@pytest.fixture
def persist_user(new_user):
    new_user.save()
    return new_user


@pytest.fixture
def persist_second_user(new_second_user):
    new_second_user.save()
    return new_second_user


@pytest.mark.django_db()
class TestUserModel():

    # In this test we delete only the profile part, and check if the profile was deleted and not the whole user
    def test_delete_only_profile_from_db(self, new_user):
        new_user.save()
        new_user.profile.delete()
        assert new_user in User.objects.all()
        assert new_user.profile not in Profile.objects.all()

    # Check invalid email
    def test_validate_email_addr(self):
        with pytest.raises(ValidationError):
            user = User(
                        username=USERNAME,
                        first_name=FIRSTNAME,
                        last_name=LASTNAME,
                        password=PASSWORD,
                        email="check")
            user.full_clean()

    # Test for unique username
    def test_unique_username(self):
        with pytest.raises(IntegrityError):
            user1 = User(
                        username="test",
                        first_name=FIRSTNAME,
                        last_name=LASTNAME,
                        password=PASSWORD,
                        email=EMAIL)
            user2 = User(
                        username="test",
                        first_name=FIRSTNAME,
                        last_name=LASTNAME,
                        password=PASSWORD,
                        email="test@gmail.com")
            user1.save()
            user2.save()

    # Test for invalid profession length
    def test_invalid_profession_length(self, new_user):
        with pytest.raises(ValidationError):
            new_user.save()
            new_user.profile.profession = LONG_PROFESSION
            new_user.profile.clean_fields()

    # Check invalid phone number
    def test_validate_phone_number(self):
        with pytest.raises(ValidationError):
            user = User(
                        username=USERNAME,
                        first_name=FIRSTNAME,
                        last_name=LASTNAME,
                        password=PASSWORD,
                        email=EMAIL)
            user.save()
            user.profile.phone_number = PHONE_NUMBER
            user.profile.clean_fields()

    # Test for invalid city
    def test_invalid_city_length(self, new_user):
        with pytest.raises(ValidationError):
            new_user.save()
            new_user.profile.city = LONG_PROFESSION
            new_user.profile.clean_fields()

    # Test for invalid account_type
    def test_invalid_account_type(self, new_user):
        with pytest.raises(ValidationError):
            new_user.save()
            new_user.profile.account_type = 'T'
            new_user.profile.clean_fields()

    # Test for invalid meeting_method
    def test_invalid_meeting_method(self, new_user):
        with pytest.raises(ValidationError):
            new_user.save()
            new_user.profile.meeting_method = 'B'
            new_user.profile.clean_fields()

    # Test for invalid bio length
    def test_invalid_bio_length(self, new_user):
        with pytest.raises(ValidationError):
            new_user.save()
            new_user.profile.bio = LONG_BIO
            new_user.profile.clean_fields()
