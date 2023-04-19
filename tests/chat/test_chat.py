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
