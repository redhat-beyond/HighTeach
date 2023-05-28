from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from course.models import StudentCourse
from study_group.models import StudyGroup


class ChatManager(models.Manager):
    def get_group_chat(self, group_id):
        return self.filter(group__study_group_id=group_id).order_by('date_time')

    def get_student_course_chat(self, student_course_id):
        return self.filter(student_course__student_course_id=student_course_id).order_by('date_time')


class Message(models.Model):
    message_id = models.BigAutoField(primary_key=True, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255, blank=False)
    objects = ChatManager()

    def clean(self):
        if self.group is not None and not self.group.is_user_in_group(self.sender):
            raise ValidationError({'sender': "The message sender is not a part of the chat group"})
        if self.student_course is not None and (
                self.student_course.student_id != self.sender and
                self.student_course.teacher_course_id.teacher_id != self.sender):
            raise ValidationError({'sender': "The message sender is not the teacher or the student of the course."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="chats_messages_student_course_or_study_group",
                check=(
                    models.Q(student_course__isnull=True, group__isnull=False)
                    | models.Q(student_course__isnull=False, group__isnull=True)
                ),
            )
        ]
