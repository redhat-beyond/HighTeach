import pytest
from study_group.models import GroupMember
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


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
        assert set([persist_user, persist_second_user]) == set(persist_group.get_all_group_members())

    def test_is_user_in_group(self, persist_group, persist_user):
        assert not persist_group.is_user_in_group(persist_user)
        persist_group.join_group(persist_user)
        assert persist_group.is_user_in_group(persist_user)

    def test_join_group_already_in(self, persist_group, persist_user):
        persist_group.join_group(persist_user)

        with pytest.raises(ValueError):
            persist_group.join_group(persist_user)

    @pytest.mark.parametrize("negative_capacity", [-2])
    def test_negative_capacity(self, new_group, negative_capacity):
        new_group.capacity = negative_capacity
        with pytest.raises(IntegrityError):
            new_group.save()

    @pytest.mark.parametrize("over_char_limit", ["Hippopotomonstrosesquippedaliophobia Support Group"])
    def test_field_over_char_limit(self, persist_group, over_char_limit):
        persist_group.field = over_char_limit
        with pytest.raises(ValidationError):
            persist_group.save()
