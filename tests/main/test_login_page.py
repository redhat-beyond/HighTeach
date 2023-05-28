import pytest
from django.urls import reverse
from conftest import USERNAME, PASSWORD, INVALID_USERNAME, INVALID_PASSWORD
from django.contrib.messages import get_messages


@pytest.mark.django_db
class TestLoginpageView:
    def test_user_login(self, client, persist_user):
        response = client.post(reverse('login'), {
            'username': USERNAME,
            'password': PASSWORD,
        })
        assert response.status_code == 200
        assert 'main/loggedInPage.html' in response.templates[0].name
        assert response.wsgi_request.user.is_authenticated

    def test_user_login_failure(self, client):
        response = client.post(reverse('login'), {
            'username': INVALID_USERNAME,
            'password': INVALID_PASSWORD,
        })
        assert response.status_code == 200
        assert 'main/login.html' in response.templates[0].name
        assert not response.wsgi_request.user.is_authenticated

    @pytest.mark.parametrize("username, password", [(INVALID_USERNAME, PASSWORD), (USERNAME, INVALID_PASSWORD)])
    def test_invalid_username_login_error_message(self, client, persist_user, username, password):
        response = client.post(reverse('login'), {
            'username': username,
            'password': password,
        })
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == "Invalid username or password."
