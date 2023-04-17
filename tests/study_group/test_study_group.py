import pytest
from study_group.models import GroupMember
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestStudyGroup:
    def test_join_group(self, persist_group, persist_user):
        persist_group.join_group(persist_user)
        assert GroupMember.objects.filter(group_id=persist_group, private_id=persist_user).exists()
        assert persist_group.group_members.count() == 1
        assert persist_group.group_members.first().private_id == persist_user

    def test_is_group_full(self, persist_group):
        for i in range(persist_group.capacity):
            assert not persist_group.is_group_full()
            persist_group.join_group(User.objects.create(username=f'user{i}', password='pass'))

        assert persist_group.is_group_full()

    def test_join_full_group(self, persist_user, persist_group):
        for i in range(persist_group.capacity):
            persist_group.join_group(User.objects.create(username=f'user{i}', password='pass'))

        with pytest.raises(ValueError):
            persist_group.join_group(persist_user)

    def test_get_all_group_members(self, persist_group, persist_user, persist_second_user):
        assert not list(persist_group.get_all_group_members())

        persist_group.join_group(persist_user)
        persist_group.join_group(persist_second_user)
        print(set(persist_group.get_all_group_members()))
        assert set([persist_user, persist_second_user]) == set(persist_group.get_all_group_members())
