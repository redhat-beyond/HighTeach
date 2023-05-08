import pytest
from .models import Profile, Account_type, Meeting_method
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.db import IntegrityError
from django.utils import timezone
# from datetime import timedelta, datetime


LAST_LOGIN = timezone.now()
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
                 "test_exceeding_max_length" * 50


PROFIL_INFORMATION = {'username': ['testusername', 'testusername2', 'testusername3'],
                      'password': ['testpassword', 'testpassword2', 'testpassword3'],
                      'first_name': ['Bob', 'john', 'jane'],
                      'last_name': ['Smith', 'Doe', 'Don'],
                      'email': ['test@test.com', 'test2@test.com', 'test3@test.com'],
                      'phone_number': ['0541234567', '0541234666', '0541234777'],
                      'account_type': [Account_type.STUDENT, Account_type.STUDENT, Account_type.STUDENT],
                      'city': ['New York', 'Tel Aviv', 'London'],
                      'meeting_method': [Meeting_method.LIVE, Meeting_method.LIVE, Meeting_method.LIVE], }


@pytest.fixture
def make_profile(idx=0):
    def make(
        username: str = PROFIL_INFORMATION.get('username')[idx],
        password: str = PROFIL_INFORMATION.get('password')[idx],
        first_name: str = PROFIL_INFORMATION.get('first_name')[idx],
        last_name: str = PROFIL_INFORMATION.get('last_name')[idx],
        email: str = PROFIL_INFORMATION.get('email')[idx],
        phone_number: str = PROFIL_INFORMATION.get('phone_number')[idx],
        account_type: str = PROFIL_INFORMATION.get('account_type')[idx],
        city: str = PROFIL_INFORMATION.get('city')[idx],
        meeting_method: str = PROFIL_INFORMATION.get('meeting_method')[idx],
    ):
        profile = Profile.create(
            username=username, password=password, account_type=account_type,
            first_name=first_name, last_name=last_name, email=email,
            phone_number=phone_number, city=city, meeting_method=meeting_method,
        )
        return profile

    return make


@pytest.fixture
def new_profile():
    return Profile.create(username=USERNAME, password=PASSWORD, account_type=Account_type.STUDENT,
                          first_name=FIRSTNAME, last_name=LASTNAME)


@pytest.mark.django_db()
class TestUserProfileModel():

    def test_profile(self, new_profile):
        assert new_profile.user.username == USERNAME
        assert new_profile.user.first_name == FIRSTNAME

    def test_profile_creation(self, new_profile):
        new_profile.save()

    def test_profile_invalid(self, new_profile):
        assert new_profile

    # Test for invalid profession length
    def test_invalid_profession_length(self, new_profile):
        with pytest.raises(ValidationError):
            new_profile.save()
            new_profile.profession = LONG_PROFESSION
            new_profile.clean_fields()

    # Test for invalid city
    def test_invalid_city_length(self, new_profile):
        with pytest.raises(ValidationError):
            new_profile.save()
            new_profile.city = LONG_PROFESSION
            new_profile.clean_fields()


@pytest.mark.django_db
class TestProfileModel:
    def test_new_profile(self, make_profile):
        profile = make_profile()
        assert profile.account_type == PROFIL_INFORMATION.get('account_type')[0]
        assert profile.phone_number == PROFIL_INFORMATION.get('phone_number')[0]
        assert profile.city == PROFIL_INFORMATION.get('city')[0]
        assert profile.meeting_method == PROFIL_INFORMATION.get('meeting_method')[0]

    def test_get_profile(self, make_profile):
        profile = make_profile()
        assert profile in Profile.objects.all()

    def test_filter_by_city(self, make_profile):
        new_profile = make_profile(username=PROFIL_INFORMATION.get('username')[1],
                                   password=PROFIL_INFORMATION.get('password')[1],
                                   email=PROFIL_INFORMATION.get('email')[1],
                                   phone_number=PROFIL_INFORMATION.get('phone_number')[1])
        make_profile(username=PROFIL_INFORMATION.get('username')[2],
                     password=PROFIL_INFORMATION.get('password')[2],
                     city='Toronto',
                     email='john2.doe@example.com',
                     phone_number='0541234636')
        make_profile(username=PROFIL_INFORMATION.get('username')[0],
                     password=PROFIL_INFORMATION.get('password')[0],
                     city='London',
                     email='john3.doe@example.com',
                     phone_number='0541234563')

        assert list(Profile.filter_by_city(PROFIL_INFORMATION.get('city')[0])) == [new_profile]

    def test_filter_by_first_name(self, make_profile):
        new_profile = make_profile(username=PROFIL_INFORMATION.get('username')[1],
                                   password=PROFIL_INFORMATION.get('password')[1],
                                   email=PROFIL_INFORMATION.get('email')[1],
                                   phone_number=PROFIL_INFORMATION.get('phone_number')[1])
        make_profile(username=PROFIL_INFORMATION.get('username')[2],
                     password=PROFIL_INFORMATION.get('password')[2],
                     first_name='David',
                     email=PROFIL_INFORMATION.get('email')[2],
                     phone_number=PROFIL_INFORMATION.get('phone_number')[2])
        make_profile(username=PROFIL_INFORMATION.get('username')[0],
                     password=PROFIL_INFORMATION.get('password')[0],
                     first_name='David',
                     email=PROFIL_INFORMATION.get('email')[0],
                     phone_number=PROFIL_INFORMATION.get('phone_number')[0])

        assert list(Profile.filter_by_first_name(PROFIL_INFORMATION.get('first_name')[0])) == [new_profile]

    def test_filter_by_last_name(self, make_profile):
        new_profile = make_profile(username=PROFIL_INFORMATION.get('username')[1],
                                   password=PROFIL_INFORMATION.get('password')[1],
                                   email=PROFIL_INFORMATION.get('email')[1],
                                   phone_number=PROFIL_INFORMATION.get('phone_number')[1])
        make_profile(username=PROFIL_INFORMATION.get('username')[2],
                     password=PROFIL_INFORMATION.get('password')[2],
                     last_name='David',
                     email=PROFIL_INFORMATION.get('email')[2],
                     phone_number=PROFIL_INFORMATION.get('phone_number')[2])
        make_profile(username=PROFIL_INFORMATION.get('username')[0],
                     password=PROFIL_INFORMATION.get('password')[0],
                     last_name='David',
                     email=PROFIL_INFORMATION.get('email')[0],
                     phone_number=PROFIL_INFORMATION.get('phone_number')[0])

        assert list(Profile.filter_by_last_name(PROFIL_INFORMATION.get('last_name')[0])) == [new_profile]
