from django.db import models
from datetime import datetime
# All the comments are to be changed after the PR merge of User and Teacher_course models
# from Teacher_course.review import Teacher_course


class ReviewManager(models.Manager):

    def get_reviews_by_course(self, course_id):
        reviews = self.filter(course_id=course_id)
        return reviews

    def get_avg_rating_by_course(self, course_id):
        avg_rating = self.filter(course_id=course_id).aggregate(models.Avg('rating'))['rating__avg']
        return avg_rating


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE_STAR = 1
        TWO_STARS = 2
        THREE_STARS = 3
        FOUR_STARS = 4
        FIVE_STARS = 5

    review_id = models.BigAutoField(primary_key=True)
    # student_id = models.ForeignKey(user, on_delete=models.CASCADE)
    # course_id = models.ForeignKey(Teacher_course, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Rating.choices)
    content = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    objects = ReviewManager()

    class Meta:
        db_table = 'Review'
