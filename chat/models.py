from django.db import models
# from django.core.exceptions import ValidationError

# class ChatManager(models.Manager):
#     def get_group_chat(self, group_id):
#         return self.filter(group_id=group_id).order_by('date_time')
#
#     def get_student_course_chat(self, student_course_id):
#         return self.filter(student_course_id=student_course_id).order_by('date_time')


class Message(models.Model):
    message_id = models.BigAutoField(primary_key=True, editable=False)
    # sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # student_course_id = models.ForeignKey(Student_Course, on_delete=models.CASCADE)
    # group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255,  blank=False)
    # objects = ChatManager()

    # def clean(self):
    #     if self.student_course_id is None and self.group_id is None:
    #         raise ValidationError({'group_id': "You can't leave both student_course_id and group_id fields as null"})
    #     elif self.student_course_id is not None and self.group_id is not None:
    #         raise ValidationError({'group_id': "One of student_course_id and group_id fields must be null"})
    #
    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super().save(*args, **kwargs)
