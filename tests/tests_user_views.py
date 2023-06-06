import pytest
from users.models import Profile, Account_type, Meeting_method
from django.test import Client
from django.urls import reverse


USERNAME = "tests_user"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "Aa313611"
EMAIL = "testuser@gmail.com"
USER_NAME_NEW = "tests_user_new"
PHONE_NUMBER = "0502220000"
CITY = "Test City"


@pytest.fixture
def new_profile():
    return Profile.create(username=USERNAME, password=PASSWORD, account_type=Account_type.STUDENT,
                          first_name=FIRSTNAME, last_name=LASTNAME)


@pytest.fixture
def login_client(client):
    client.login(username='testuser', password='testpassword')
    return client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def valid_registration_data():
    return {
        'username': 'test_user',
        'email': 'test_user@test.com',
        'password1': 'test_password',
        'password2': 'test_password',
        'account_type': Account_type.TEACHER,
        'phone_number': '+1234567890',
        'city': 'Test City',
        'meeting_method': Meeting_method.LIVE
    }


@pytest.mark.django_db
class TestProfileViews:
    def test_users_detail_view_loaded_authorized(self, authorized_client, persist_user_profile):
        users_detail_response = authorized_client.get(f'/users/{persist_user_profile.user.username}/', follow=True)
        assert users_detail_response.status_code == 200
        assert 'profile_details.html' in users_detail_response.templates[0].name

    def test_users_detail_view_loaded_unauthorized(self, client, persist_user_profile):
        users_detail_response = client.get(f'/users/{persist_user_profile.user.username}/', follow=True)
        assert users_detail_response.status_code == 200
        assert 'main/login.html' in users_detail_response.templates[0].name

    def test_edit_profile_view_unauthenticated(self, client, new_profile):
        url = reverse('users-edit-profile', kwargs={'slug': new_profile.user.username})
        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert 'main/login.html' in response.templates[0].name

    def test_edit_profile_view_authenticated(self, login_client, new_profile):
        url = reverse('users-edit-profile', kwargs={'slug': new_profile.user.username})
        response = login_client.get(url, follow=True)
        assert response.status_code == 200
        assert 'main/login.html' in response.templates[0].name

    def test_users_update_view_loaded_authorized(self, authorized_client, persist_user_profile):
        user_detail_response = authorized_client.get(f"/users/{persist_user_profile.pk}/edit-profile/")
        assert user_detail_response.status_code == 200
        assert 'edit-profile.html' in user_detail_response.templates[0].name

    @pytest.mark.parametrize("email, city", [(EMAIL, "city_test")])
    def test_update_user(self, persist_user_profile, authorized_client, email, city):

        profile = Profile.objects.filter(user=persist_user_profile.user).first()
        assert profile.city != city
        assert profile.user.email != email

        new_profile = {"username": persist_user_profile.user.username,
                       "email": email,
                       "first_name": "",
                       "last_name": "",
                       "bio": "",
                       "profession": "",
                       "city": city,
                       "phone_number": '0500000000',
                       "account_type": 'B',
                       "meeting_method": "B"}

        response = authorized_client.post(f"/users/{persist_user_profile.user.username}/edit-profile/",
                                          new_profile, follow=True)
        profile = Profile.objects.filter(user=persist_user_profile.user).first()
        assert response.status_code == 200
        assert profile.city == city
        assert profile.user.email == email
        assert 'main/loggedInPage.html' in response.templates[0].name

    def test_register_page_load(self, client):
        profile_response = client.get('/register', follow=True)
        assert profile_response.status_code == 200
        assert 'register.html' in profile_response.templates[0].name

    def test_register_views_respone(self, client, valid_registration_data):
        response = client.post('/register/', valid_registration_data)
        assert response.status_code == 302
        assert response.url == '/'

    @pytest.mark.parametrize("username, password1, password2, account_type",
                             [("user_name", PASSWORD, PASSWORD, Account_type.TEACHER)])
    def test_create_new_profile(self, authorized_client, username, password1, password2, account_type):
        profile_creation_form_args = {"username": username, "password1": password1, "password2": password2,
                                      "account_type": account_type}

        assert not Profile.objects.filter(user__username=username).exists()
        profile_creation_response = authorized_client.post("/register/", profile_creation_form_args, follow=True)
        assert profile_creation_response.status_code == 200
        assert 'users/register.html' in profile_creation_response.templates[0].name
