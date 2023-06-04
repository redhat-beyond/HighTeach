import pytest
from chat.models import Message
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestMessage:
    def test_message_save_with_group(self, message_with_group):
        message_with_group.save()
        assert message_with_group in Message.objects.all()

    def test_message_save_with_student_course_id(self, message_with_student_course):
        message_with_student_course.save()
        assert message_with_student_course in Message.objects.all()

    def test_message_save_with_both_group_and_course_id(self, persist_user, student_course0, study_group0):
        message = Message(sender=persist_user, group=study_group0, student_course=student_course0, message='test')

        with pytest.raises(ValidationError):
            message.save()

    def test_message_save_without_group_and_course_id(self):
        message = Message(message='test')

        with pytest.raises(ValidationError):
            message.save()

    def test_message_save_with_group_invalid_sender(self, study_group0, user_without_group_and_course):
        message = Message(sender=user_without_group_and_course, group=study_group0, message='test')

        with pytest.raises(ValidationError):
            message.save()

    def test_message_save_with_student_course_invalid_sender(self, student_course0, user_without_group_and_course):
        message = Message(sender=user_without_group_and_course, student_course=student_course0, message='test')

        with pytest.raises(ValidationError):
            message.save()


@pytest.mark.django_db
class TestChatManager:
    def test_get_group_chat(self, message_with_group):
        message_with_group.save()

        group_messages = Message.objects.get_group_chat(group_id=message_with_group.group.study_group_id)

        assert message_with_group in group_messages

    def test_get_group_chat_different_group_id(self, message_with_group):
        message_with_group.save()

        group_messages = Message.objects.get_group_chat(group_id=message_with_group.group.study_group_id + 1)

        assert message_with_group not in group_messages

    def test_get_student_course_chat(self, message_with_student_course):
        message_with_student_course.save()

        course_messages = Message.objects.get_student_course_chat(
            student_course_id=message_with_student_course.student_course.student_course_id)

        assert message_with_student_course in course_messages


@pytest.mark.django_db
class TestChatAPI:
    def test_get_student_course_chat(self, client, persist_second_user, student_course0,
                                     persist_message_with_student_course):
        client.force_login(user=persist_second_user)
        response = client.get(f'/chat/courses/{student_course0.student_course_id}')
        response_message_ids = [m['message_id'] for m in response.data]

        assert persist_message_with_student_course.message_id in response_message_ids
        assert response.status_code == 200

    def test_get_student_course_chat_not_logged_in(self, client, student_course0, persist_message_with_student_course):
        response = client.get(f'/chat/courses/{student_course0.student_course_id}')
        assert response.status_code == 401

    def test_get_student_course_chat_not_in_course(self, client, persist_teacher, student_course0,
                                                   persist_message_with_student_course):
        client.force_login(user=persist_teacher)
        response = client.get(f'/chat/courses/{student_course0.student_course_id}')
        assert response.status_code == 401

    def test_add_message_to_course_chat(self, client, persist_second_user, student_course0,
                                        add_message_to_course_request_data):
        chat_messages = Message.objects.get_student_course_chat(student_course0.student_course_id)
        len_messages_before_post = len(chat_messages)
        client.force_login(user=persist_second_user)
        client.post('/chat/post-message/', add_message_to_course_request_data)
        chat_messages_after_post = Message.objects.get_student_course_chat(student_course0.student_course_id)
        assert len(chat_messages_after_post) == len_messages_before_post + 1

    def test_add_message_to_course_chat_not_logged_in(self, client, student_course0,
                                                      add_message_to_course_request_data):
        chat_messages = Message.objects.get_student_course_chat(student_course0.student_course_id)
        len_messages_before_post = len(chat_messages)
        response = client.post('/chat/post-message/', add_message_to_course_request_data)
        chat_messages_after_post = Message.objects.get_student_course_chat(student_course0.student_course_id)
        assert len(chat_messages_after_post) == len_messages_before_post
        assert response.status_code == 401

    def test_add_message_to_course_chat_not_in_course(self, client, persist_teacher, student_course0,
                                                      add_message_to_course_request_data):
        chat_messages = Message.objects.get_student_course_chat(student_course0.student_course_id)
        len_messages_before_post = len(chat_messages)
        client.force_login(user=persist_teacher)
        response = client.post('/chat/post-message/', add_message_to_course_request_data)
        chat_messages_after_post = Message.objects.get_student_course_chat(student_course0.student_course_id)
        assert len(chat_messages_after_post) == len_messages_before_post
        assert response.status_code == 400

    def test_get_study_group_chat(self, client, persist_user, study_group0, persist_message_with_group):
        client.force_login(user=persist_user)
        response = client.get(f'/chat/groups/{study_group0.study_group_id}')
        response_message_ids = [m['message_id'] for m in response.data]

        assert persist_message_with_group.message_id in response_message_ids
        assert response.status_code == 200

    def test_add_message_to_group_chat(self, client, persist_user, study_group0, add_message_to_group_request_data):
        chat_messages = Message.objects.get_group_chat(study_group0.study_group_id)
        len_messages_before_post = len(chat_messages)
        client.force_login(user=persist_user)
        client.post('/chat/post-message/', add_message_to_group_request_data)
        chat_messages_after_post = Message.objects.get_group_chat(study_group0.study_group_id)
        assert len(chat_messages_after_post) == len_messages_before_post + 1

    def test_add_message_to_group_chat_not_logged_in(self, client, study_group0, add_message_to_group_request_data):
        chat_messages = Message.objects.get_group_chat(study_group0.study_group_id)
        len_messages_before_post = len(chat_messages)
        response = client.post('/chat/post-message/', add_message_to_group_request_data)
        chat_messages_after_post = Message.objects.get_group_chat(study_group0.study_group_id)
        assert len(chat_messages_after_post) == len_messages_before_post
        assert response.status_code == 401

    def test_add_message_to_group_chat_not_in_group(self, client, persist_second_user, study_group0,
                                                    add_message_to_group_request_data):
        chat_messages = Message.objects.get_group_chat(study_group0.study_group_id)
        len_messages_before_post = len(chat_messages)
        client.force_login(user=persist_second_user)
        response = client.post('/chat/post-message/', add_message_to_group_request_data)
        chat_messages_after_post = Message.objects.get_group_chat(study_group0.study_group_id)
        assert len(chat_messages_after_post) == len_messages_before_post
        assert response.status_code == 400

    def test_get_study_group_chat_not_logged_in(self, client, study_group0, persist_message_with_group):
        response = client.get(f'/chat/groups/{study_group0.study_group_id}')
        assert response.status_code == 401

    def test_get_study_group_chat_not_in_group(self, client, persist_second_user, study_group0,
                                               persist_message_with_group):
        client.force_login(user=persist_second_user)
        response = client.get(f'/chat/groups/{study_group0.study_group_id}')
        assert response.status_code == 401
