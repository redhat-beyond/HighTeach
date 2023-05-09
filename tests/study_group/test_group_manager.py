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

    def test_search_group_by_keyword(self, persist_group, persist_second_group):
        empty = StudyGroup.objects.search_group_by_keyword("this keyword should not exist")
        assert not empty

        math_keyword_set = StudyGroup.objects.search_group_by_keyword("cs")
        assert list(math_keyword_set) == [persist_group]

        guitar_keyword_set = StudyGroup.objects.search_group_by_keyword("guitar")
        assert list(guitar_keyword_set) == [persist_second_group]

        groups_keyword_set = StudyGroup.objects.search_group_by_keyword("fixture")
        assert set(groups_keyword_set) == set([persist_group, persist_second_group])

    def test_get_all_groups_for_user(self, persist_user, persist_group, persist_second_group):
        persist_group.join_group(persist_user)

        assert list(StudyGroup.objects.get_groups_by_user(persist_user)) == [persist_group]
