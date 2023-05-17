import pytest
from django.urls import reverse

from study_group.models import StudyGroup


@pytest.mark.django_db
class TestStudyGroupDetailView:
    def test_study_group_detail_view_loaded_authorized(self, authorized_client, persist_group):
        group_detail_response = authorized_client.get(f"/study-group/detail/{persist_group.pk}/")
        assert group_detail_response.status_code == 200
        assert 'study_group_detail.html' in group_detail_response.templates[0].name

    def test_study_group_detail_view_loaded_unauthorized(self, client, persist_group):
        study_group_list_response = client.get(f"/study-group/detail/{persist_group.pk}/")
        assert study_group_list_response.status_code == 302

    def test_display_edit_group_when_owner(self, client, persist_user, persist_group):
        client.force_login(persist_user)
        response = client.get(f"/study-group/detail/{persist_group.pk}/")
        assert b"Edit Group info" in response.content

    def test_not_display_edit_group_when_not_owner(self, client, persist_second_user, persist_group):
        client.force_login(persist_second_user)
        response = client.get(f"/study-group/detail/{persist_group.pk}/")
        assert b"Edit Group info" not in response.content


@pytest.mark.django_db
class TestStudyGroupUpdateView:
    def test_study_group_update_view_loaded_authorized(self, authorized_client, persist_group):
        group_detail_response = authorized_client.get(f"/study-group/update/{persist_group.pk}/")
        assert group_detail_response.status_code == 200
        assert 'study_group_update.html' in group_detail_response.templates[0].name

    @pytest.mark.parametrize("new_field, new_desc", [("new field", "this is a new group description")])
    def test_update_group_details_not_owner(self, make_study_group_of_varied_size, authorized_client, new_field,
                                            new_desc):
        group_not_owner_of = make_study_group_of_varied_size(1, 5)
        response = authorized_client.post(f"/study-group/update/{group_not_owner_of.pk}/",
                                          {"field": new_field, "group_description": new_desc})
        assert response.status_code == 403


@pytest.mark.django_db
class TestJoinLeaveGroupButton:
    def test_leave_group(self, client, persist_user, persist_group):
        client.force_login(persist_user)
        persist_group.join_group(persist_user)
        assert persist_group.is_user_in_group(persist_user)

        post_response = client.post(f"/study-group/join_leave/{persist_group.pk}/")

        assert post_response.status_code == 302
        assert post_response.url == reverse("study_group_detail", kwargs={"pk": persist_group.pk})
        assert not persist_group.is_user_in_group(persist_user)

    def test_join_group(self, client, persist_user, persist_group):
        client.force_login(persist_user)
        assert not persist_group.is_user_in_group(persist_user)

        post_response = client.post(f"/study-group/join_leave/{persist_group.pk}/")

        assert post_response.status_code == 302
        assert post_response.url == reverse("study_group_detail", kwargs={"pk": persist_group.pk})
        assert persist_group.is_user_in_group(persist_user)

    def test_join_leave_non_existent_group(self, authorized_client, persist_group):
        StudyGroup.objects.get(pk=persist_group.pk).delete()
        post_response = authorized_client.post(f"/study-group/join_leave/{persist_group.pk}/")

        assert post_response.status_code == 404

    @pytest.mark.parametrize("non_full, capacity", [(0, 5)])
    def test_join_group_button_text(self, make_study_group_of_varied_size, authorized_client,
                                    non_full, capacity):
        non_empty_group = make_study_group_of_varied_size(non_full, capacity)
        response = authorized_client.get(f"/study-group/detail/{non_empty_group.pk}/")
        assert b"Join Group" in response.content

    @pytest.mark.parametrize("full, capacity", [(1, 1)])
    def test_full_group_button_text(self, make_study_group_of_varied_size, authorized_client,
                                    full, capacity):
        non_empty_group = make_study_group_of_varied_size(full, capacity)
        response = authorized_client.get(f"/study-group/detail/{non_empty_group.pk}/")
        assert b"Group Full" in response.content

    @pytest.mark.parametrize("num_of_members, capacity", [(1, 2)])
    def test_leave_group_text_button(self, make_study_group_of_varied_size, num_of_members, capacity,
                                     persist_user, client):
        study_group = make_study_group_of_varied_size(num_of_members, capacity)
        study_group.join_group(persist_user)

        client.force_login(persist_user)
        response = client.get(f"/study-group/detail/{study_group.pk}/")
        assert b"Leave Group" in response.content
