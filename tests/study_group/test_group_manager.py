import pytest
from study_group.models import StudyGroup
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestStudyGroupManager:
    def test_get_all_non_full_groups(self, persist_group, persist_second_group):
        for i in range(persist_group.capacity):
            persist_group.join_group(User.objects.create(username=f'user{i}', password='pass'))

        result = StudyGroup.objects.get_all_non_full_groups()
        assert persist_group not in result
        assert persist_second_group in result

    @pytest.mark.parametrize("keyword, expected",
                             [("this keyword should not exist", []),
                              ("math", ["persist_group"]),
                              ("guitar", ["persist_second_group"]),
                              ("group", ["persist_group", "persist_second_group"])]
                             )
    def test_search_group_by_keyword(self, keyword, expected, request):
        expected = request.getfixturevalue(expected)
        assert list(StudyGroup.objects.search_group_by_keyword(keyword)) == list(expected)
