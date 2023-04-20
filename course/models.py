from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

Category = [
    ('BUSINESS_AND_MANAGEMENT', 'Business & Management'),
    ('COMPUTER_SCIENCE_AND_IT', 'Computer Science & IT'),
    ('CREATIVE_ARTS', 'Creative Arts'),
    ('ECONOMICS', 'Economics'),
    ('HISTORY', 'History'),
    ('HEALTH_AND_PSYCHOLOGY', 'Health & Psychology'),
    ('LITERATURE', 'Literature'),
    ('LAW', 'Law'),
    ('LANGUAGES_AND_CULTURES', 'Languages & Cultures'),
    ('MATHS', 'Maths'),
    ('MARKETING', 'Marketing'),
    ('OTHER', 'Other'),
    ('POLITICS_AND_SOCIETY', 'Politics & Society'),
    ('SCIENCE_AND_ENGINEERING', 'Science & Engineering'),
    ('SPORT_AND_LEISURE', 'Sport & Leisure'),
]

Level = [
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),
]


class TeacherCoursesManager(models.Manager):

    def in_price_range(self, min: int, max: int):
        return self.filter(price__lte=max, price__gte=min)

    def in_category(self, cat: str):
        return self.filter(category=cat)

    def got_experience(self, exp: int):
        if exp > 5:
            exp = 5
        return self.filter(years_of_experience__gte=exp)

    def search_name(self, keyword: str):
        return self.filter(Q(course_name__icontains=keyword) | Q(description__icontains=keyword))

    def get_level(self, level: str):
        return self.filter(difficulty_level=level)

    def get_teacher_courses(self, id: int):
        return self.filter(teacher_id=id)


class TeacherCourses(models.Model):
    course_id = models.BigAutoField(primary_key=True)
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=30, blank=False)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0, blank=False)
    objects = TeacherCoursesManager()

    class Experience(models.IntegerChoices):
        ZERO = 0, _("0")
        ONE = 1, _("1")
        TWO = 2, _("2")
        THREE = 3, _("3")
        FOUR = 4, _("4")
        FIVE_PLUS = 5, _("5+")

    years_of_experience = models.IntegerField(
        choices=Experience.choices,
        default=Experience.ZERO
    )

    difficulty_level = models.CharField(
        max_length=30,
        choices=Level,
    )

    category = models.CharField(
        max_length=30,
        choices=Category,
    )

    def get_experience(self):
        # Function for display in Admin
        return self.Experience.choices[int(self.years_of_experience)][1]

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Teacher Courses"


class ReviewManager(models.Manager):

    def get_reviews_by_course(self, course_id: int):
        reviews = Review.objects.filter(course_id=course_id)
        return reviews

    def get_avg_rating_by_course(self, course_id: int):
        avg_rating = self.filter(course_id=course_id).aggregate(models.Avg('rating'))['rating__avg']
        return avg_rating

    def get_number_of_review_of_course(self, course_id):
        return len(self.filter(course_id=course_id))


class Review(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(TeacherCourses, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    content = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    objects = ReviewManager()


class StudentCoursesManager(models.Manager):

    def get_teacher_pending(self, id: int):
        return TeacherCourses.objects.get_teacher_courses(id).values("course_id").intersection(
            self.filter(status=Status.PENDING).values("teacher_course_id")).values_list(flat=True)

    def get_student_pending(self, id: int):
        return self.filter(student_id=id, status=Status.PENDING)

    def get_student_courses(self, id: int):
        return self.filter(student_id=id)


class Status(models.TextChoices):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'


class StudentCourses(models.Model):
    student_course_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher_course_id = models.ForeignKey(TeacherCourses, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    objects = StudentCoursesManager()

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def change_to_confirmed(self):
        self.status = Status.CONFIRMED.value
        self.save()

    def clean(self):
        if self.teacher_course_id.teacher_id == self.student_id:
            raise ValidationError({'teacher_course_id': "Can't create a request to your own course"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.student_course_id)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Student Courses"
        constraints = [models.UniqueConstraint(fields=['student_id', 'teacher_course_id'],
                                               name="Already have a pending/confirmed request in this course")]
