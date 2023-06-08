import pytest
from course.models import Review
from django.core.validators import ValidationError
from datetime import date


@pytest.fixture
def make_review():
    def _make_review(persist_user, persist_course):
        new_review = Review(student=persist_user, course=persist_course,
                            rating=1, content=f"Review by {persist_user} for {persist_course.course_id}",
                            date=date(2023, 4, 17))
        new_review.save()
        return new_review

    return _make_review


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

    def test_check_if_review_exist_by_student(self, make_review, persist_user, persist_course):
        review = Review.objects.check_if_review_exist_by_student(persist_user, persist_course)
        assert review is None
        make_review(persist_user, persist_course)
        review_by_student = Review.objects.check_if_review_exist_by_student(persist_user, persist_course)
        assert review_by_student is not None

    def test_get_review_in_course_by_student(self, persist_review):
        review = Review.objects.get_review_in_course_by_student(persist_review.student, persist_review.course)
        assert review.pk == persist_review.pk
