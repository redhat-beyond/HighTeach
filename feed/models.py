from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.contrib.auth.models import User
from course.models import TeacherCourses, StudentCourses


class PostManager(models.Manager):
    @staticmethod
    def get_posts_for_user(user: User):
        relevant_users = StudentCourses.objects.filter(
            Q(Q(student_id=user) & Q(status="Confirmed")) | Q(teacher_course_id__teacher_id=user)
        )
        relevant_courses = TeacherCourses.objects.filter(studentcourses__in=relevant_users).distinct()
        relevant_posts = Post.objects.filter(course_id__in=relevant_courses).order_by("date")

        # create the post hierarchy in a dictionary that contains lists
        post_hierarchy = {}
        for post in relevant_posts:
            if post.parent_post_id:
                post_hierarchy[post.parent_post_id].append(post)
            else:
                post_hierarchy[post] = []

        return post_hierarchy


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(TeacherCourses, on_delete=models.CASCADE, related_name="related_posts")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post_id = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False)
    objects = PostManager()

    def is_root_post(self):
        return self.parent_post_id is None

    @staticmethod
    def is_user_able_to_post_in_course(user, course):
        return StudentCourses.objects.filter(
            Q(Q(student_id=user) & Q(status="Confirmed")) | Q(teacher_course_id=course)
        ).exists()

    def clean(self):
        if self.parent_post_id and self.parent_post_id.parent_post_id:
            raise ValidationError("Replies can only be made directly to the original post")
        if not self.is_user_able_to_post_in_course(self.user_id, self.course_id):
            raise ValidationError("User is not course owner or participant")
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_id} | {self.user_id}: {self.content}"

