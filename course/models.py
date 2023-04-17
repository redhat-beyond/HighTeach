from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# import user

# All the comments are to be changed after the PR merge of User and Teacher_course models


class ReviewManager(models.Manager):

    def get_reviews_by_course(self, course_id: int):
        reviews = self.filter(course_id=course_id)
        return reviews

    def get_avg_rating_by_course(self, course_id: int):
        avg_rating = self.filter(course_id=course_id).aggregate(models.Avg('rating'))['rating__avg']
        return avg_rating


class Review(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    # student_id = models.ForeignKey(user, on_delete=models.CASCADE)
    # course_id = models.ForeignKey(Teacher_course, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    content = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    objects = ReviewManager()
