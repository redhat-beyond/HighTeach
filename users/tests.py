import pytest
from .models import Profile, Account_type
from django.core.exceptions import ValidationError
from django.utils import timezone


LAST_LOGIN = timezone.now()
CREATION_DATE = timezone.now()
USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
PHONE_NUMBER = "0541234567"
LONG_PROFESSION = "test_exceeding_max_length" * 80


@pytest.fixture
def make_profile():
    def make(idx, account_type):
        profile = Profile.create(
            username=f"username{idx}", password=f"password{idx}", account_type=account_type,
            first_name=f"first_name{idx}", last_name=f"last_name{idx}", email=f"email{idx}",
            city=f"city{idx}",
        )
        return profile

    return make


@pytest.fixture
def new_profile():
    return Profile.create(username=USERNAME, password=PASSWORD, account_type=Account_type.STUDENT,
                          first_name=FIRSTNAME, last_name=LASTNAME)


@pytest.mark.django_db
class TestProfileModel:
    def test_invalid_city_length(self, new_profile):
        with pytest.raises(ValidationError):
            new_profile.save()
            new_profile.city = LONG_PROFESSION
            new_profile.clean_fields()

    @pytest.mark.parametrize("user_idx, account_type", [(1, Account_type.STUDENT)])
    def test_create_new_profile(self, make_profile, user_idx, account_type):
        profile = make_profile(user_idx, account_type)
        assert profile.account_type == account_type
        assert profile.user.username == f"username{user_idx}"
        assert profile.user.first_name == f"first_name{user_idx}"
        assert profile.user.last_name == f"last_name{user_idx}"
        assert profile.user.email == f"email{user_idx}"
        assert profile.city == f"city{user_idx}"

    @pytest.mark.parametrize("user_idx, account_type, second_user_idx, second_account_type",
                             [(1, Account_type.STUDENT, 2, Account_type.TEACHER)])
    def test_filter_by_city(self, make_profile, user_idx, account_type, second_user_idx, second_account_type):
        new_profile = make_profile(user_idx, account_type)
        make_profile(second_user_idx, second_account_type)
        profiles_by_city = Profile.filter_by_city(new_profile.city)
        assert sorted(list(profiles_by_city)) == [new_profile]

    @pytest.mark.parametrize("user_idx, account_type, second_user_idx, second_account_type",
                             [(1, Account_type.STUDENT, 2, Account_type.TEACHER)])
    def test_filter_by_first_name(self, make_profile, user_idx, account_type, second_user_idx, second_account_type):
        new_profile = make_profile(user_idx, account_type)
        make_profile(second_user_idx, second_account_type)
        profiles_by_first_name = Profile.filter_by_first_name(new_profile.user.first_name)
        assert sorted(list(profiles_by_first_name)) == [new_profile]

    @pytest.mark.parametrize("user_idx, account_type, second_user_idx, second_account_type",
                             [(1, Account_type.STUDENT, 2, Account_type.TEACHER)])
    def test_filter_by_last_name(self, make_profile, user_idx, account_type, second_user_idx, second_account_type):
        new_profile = make_profile(user_idx, account_type)
        make_profile(second_user_idx, second_account_type)
        profiles_by_last_name = Profile.filter_by_last_name(new_profile.user.last_name)
        assert sorted(list(profiles_by_last_name)) == [new_profile]

    @pytest.mark.parametrize("user_idx, account_type, second_user_idx, second_account_type",
                             [(1, Account_type.STUDENT, 2, Account_type.TEACHER)])
    def test_filter_by_account_type(self, make_profile, user_idx, account_type, second_user_idx, second_account_type):
        new_profile = make_profile(user_idx, account_type)
        make_profile(second_user_idx, second_account_type)
        profiles_by_account_type = Profile.filter_by_account_type(new_profile.account_type)
        assert sorted(list(profiles_by_account_type)) == [new_profile]
