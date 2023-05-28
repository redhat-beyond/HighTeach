import pytest


@pytest.mark.django_db
class TestHomepageView:
    def test_successful_logout(self, client, persist_user):
        client.force_login(user=persist_user)
        response = client.get('/logout/')
        assert response.status_code == 200
        assert response.wsgi_request.user.is_anonymous

    def test_extends_of_base(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert 'homePage.html' in response.templates[0].name
        assert b'Login' in response.content
        assert b'Register' in response.content

    def test_logged_user(self, client, persist_user):
        client.force_login(persist_user)
        response = client.get('/')
        assert response.status_code == 200
        assert 'loggedInPage.html' in response.templates[0].name
        assert b'Logout' in response.content
