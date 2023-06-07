import pytest
from django.urls import reverse
from course.models import Review
from django.contrib.messages import get_messages


@pytest.mark.django_db
class TestReviewView:
    def test_add_review(self, authorized_second_client, new_review):
        course_response = authorized_second_client.get('/course/' + str(new_review.course_id))
        assert course_response.status_code == 200
        response = authorized_second_client.post(f'/course/{new_review.course_id}/add_review',
                                                 {'rating': new_review.rating, 'content': new_review.content})
        assert response.status_code == 302
        assert Review.objects.exists()

    def test_invalid_review_message(self, authorized_second_client, new_review):
        response = authorized_second_client.post(f'/course/{new_review.course_id}/add_review',
                                                 {'content': new_review.content})
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == "You must enter rating"

    def test_display_review_existed(self, authorized_second_client, persist_review):
        response = authorized_second_client.get('/course/' + str(persist_review.course_id), {'review_view': True})
        assert response.status_code == 200
        assert Review.objects.count() == 1
        assert b"Update Review" in response.content
        assert b"Delete Review" in response.content
        assert b"Add Review" not in response.content

    def test_display_review_not_existed(self, authorized_second_client, new_review):
        response = authorized_second_client.get('/course/' + str(new_review.course_id), {'review_view': False})
        assert response.status_code == 200
        assert Review.objects.count() == 0
        assert b"Add Review" in response.content
        assert b"Update Review" not in response.content
        assert b"Delete Review" not in response.content

    @pytest.mark.parametrize("rating, content", [(4, "Updated review content")])
    def test_update_review(self, authorized_second_client, persist_review, rating, content):
        response = authorized_second_client.post(f'/course/{persist_review.course_id}/update_review',
                                                 {'rating': rating, 'content': content})
        assert response.status_code == 302
        updated_review = Review.objects.get_reviews_by_course(course=persist_review.course_id)[0]
        assert persist_review.pk == updated_review.pk
        assert updated_review.rating == rating
        assert updated_review.content == content

    def test_delete_review(self, authorized_second_client, persist_review):
        response = authorized_second_client.post(reverse('delete_review', args=[persist_review.course_id]))
        assert response.status_code == 302
        assert not Review.objects.filter(pk=persist_review.pk).exists()

    def test_show_reviews_view(self, authorized_second_client, persist_review):
        response = authorized_second_client.get('/course/' + str(persist_review.course_id))
        assert response.status_code == 200
        assert any(persist_review.pk == review.pk for review in response.context['reviews'])

    def test_show_without_reviews_view(self, authorized_second_client, persist_course):
        response = authorized_second_client.get('/course/' + str(persist_course.course_id))
        reviews_by_course = response.context['reviews']
        assert response.status_code == 200
        assert list(reviews_by_course) == []
        assert b"No reviews available" in response.content

    def test_display_teacher_add_review_not_existed(self, client, persist_teacher, new_review):
        client.force_login(persist_teacher)
        response = client.get('/course/' + str(new_review.course_id))
        assert response.status_code == 200
        assert Review.objects.count() == 0
        assert b"Add Review" not in response.content
