import pytest

from django.urls import reverse

from users.models import Profile
from study_group.models import StudyGroup
from course.models import TeacherCourse


@pytest.fixture
def make_search_http_response_from_query_param(authorized_client):
    def _make_search_http_response_from_query_param(search_query_param):
        search_url = f"{reverse('search')}?q={search_query_param}"
        return authorized_client.get(search_url)

    return _make_search_http_response_from_query_param


@pytest.mark.django_db
class TestStudyGroupDetailView:
    @pytest.mark.parametrize("search_query_param", ["test"])
    def test_search_view_loaded_authorized(self, make_search_http_response_from_query_param, search_query_param):
        search_response = make_search_http_response_from_query_param(search_query_param)
        assert search_response.status_code == 200
        assert 'search.html' in search_response.templates[0].name

    @pytest.mark.parametrize("search_query_param", ["test"])
    def test_search_view_loaded_unauthorized(self, client, search_query_param):
        search_response = client.get(f"{reverse('search')}?q={search_query_param}")
        assert search_response.status_code == 302

    @pytest.mark.parametrize("search_query_param, study_group_context_name", [("", "study_groups"),
                                                                              ("a", "study_groups"),
                                                                              ("math", "study_groups"),
                                                                              ("group", "study_groups")])
    def test_search_context_equals_expected_queryset_study_groups(self, make_search_http_response_from_query_param,
                                                                  search_query_param, study_group_context_name):
        search_response = make_search_http_response_from_query_param(search_query_param)

        expected_study_group_queryset = StudyGroup.objects.search_group_by_keyword(search_query_param)
        given_study_group_queryset = search_response.context[study_group_context_name]

        assert set(expected_study_group_queryset) == set(given_study_group_queryset)

    @pytest.mark.parametrize("search_query_param, users_context_name", [("", "users"), ("a", "users"),
                                                                        ("user", "users"), ("history", "users")])
    def test_search_context_equals_expected_queryset_users(self, make_search_http_response_from_query_param,
                                                           search_query_param, users_context_name):
        search_response = make_search_http_response_from_query_param(search_query_param)

        expected_users_queryset = Profile.search_users_by_keyword(search_query_param)
        given_users_queryset = search_response.context[users_context_name]

        assert set(expected_users_queryset) == set(given_users_queryset)

    @pytest.mark.parametrize("search_query_param, courses_context_name", [("", "teacher_courses"),
                                                                          ("course", "teacher_courses"),
                                                                          ("a", "teacher_courses"),
                                                                          ("linear", "teacher_courses")])
    def test_search_context_equals_expected_queryset_courses(self, make_search_http_response_from_query_param,
                                                             search_query_param, courses_context_name):
        search_response = make_search_http_response_from_query_param(search_query_param)

        expected_courses_queryset = TeacherCourse.objects.search_name(search_query_param)
        given_courses_queryset = search_response.context[courses_context_name]

        assert set(expected_courses_queryset) == set(given_courses_queryset)
