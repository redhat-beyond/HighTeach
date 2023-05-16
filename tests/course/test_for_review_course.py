import pytest
from course.models import Review
from django.core.validators import ValidationError


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
