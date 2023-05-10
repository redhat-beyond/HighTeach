import pytest
from django.contrib.auth.models import User
from course.models import Review, TeacherCourse
from django.core.validators import ValidationError
from datetime import date


@pytest.fixture
def new_user():
    user = User(username="test3",
                first_name="test",
                last_name="mctest",
                email="test1@gmail.com")

    user.set_password("PASSWORD")
    return user


@pytest.fixture
def new_user_number_two():
    user = User(username="natali",
                first_name="shiraz",
                last_name="yom tov",
                email="shiraz@gmail.com")

    user.set_password("PASSWORD2")
    return user


@pytest.fixture
def new_teacher_course(persist_user):
    teacher_course = TeacherCourse(course_id=1, teacher_id=persist_user, difficulty_level='B',
                                   category='MATHS', course_name="Math",
                                   description="course", price=70)
    return teacher_course


@pytest.fixture
def new_review(persist_user_number_two, persist_teacher_course):
    review = Review(student=persist_user_number_two, course=persist_teacher_course,
                    rating=1, content="Greate course", date=date(2023, 4, 17))
    return review


@pytest.fixture
def new_review_two(persist_user, persist_teacher_course):
    review = Review(student=persist_user, course=persist_teacher_course,
                    rating=2, content="Greate course", date=date(2023, 4, 17))
    return review


@pytest.fixture
def persist_user(new_user):
    new_user.save()
    return new_user


@pytest.fixture
def persist_user_number_two(new_user_number_two):
    new_user_number_two.save()
    return new_user_number_two


@pytest.fixture
def persist_teacher_course(new_teacher_course):
    new_teacher_course.teacher_id.save()
    new_teacher_course.save()
    return new_teacher_course


@pytest.fixture
def persist_teacher_course_number_two(new_teacher_course_number_two):
    new_teacher_course_number_two.teacher_id.save()
    new_teacher_course_number_two.save()
    return new_teacher_course_number_two


@pytest.fixture
def persist_review(new_review):
    new_review.save()
    return new_review


@pytest.fixture
def persist_review_number_two(new_review_two):
    new_review_two.save()
    return new_review_two


@pytest.mark.django_db()
class TestReview:
    @pytest.mark.parametrize("rating", [0, 6])
    def test_rating_limit(self, rating, new_review):
        new_review.rating = rating
        with pytest.raises(ValidationError):
            new_review.full_clean()

    def test_review_average_function(self, persist_review, persist_review_number_two):
        assert Review.objects.get_avg_rating_by_course(1) == 1.5

    def test_get_review_by_course(self, persist_review):
        assert [persist_review] == list(Review.objects.get_reviews_by_course(course=1))

    def test_student_reviewer(self, persist_review):
        assert persist_review.student.username != persist_review.course.teacher_id.username

    def test_get_number_of_review_of_course(self, persist_review, persist_review_number_two):
        result = Review.objects.get_number_of_review_of_course(persist_review.course)
        assert result == 2
