import pytest
from django.urls import reverse
from course.models import Review
from django.contrib.messages import get_messages


@pytest.mark.django_db
class TestReviewView:
    def test_create_review(self, client, persist_user, persist_review):
        client.force_login(persist_user)
        response = client.post(reverse('create_review', args=[persist_review.course_id]), {
            'rating': persist_review.rating,
            'content': persist_review.content
        })
        assert response.status_code == 302
        assert Review.objects.exists()

    def test_invalid_review_message(self, client, persist_user, persist_review):
        client.force_login(persist_user)
        response = client.post(reverse('create_review', args=[persist_review.course_id]), {
            'content': persist_review.content
        })
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == "You must enter rating"

    def test_update_review(self, client, persist_user, persist_review):
        client.force_login(persist_user)
        response = client.post(reverse('update_review', args=[persist_review.pk]),
                               data={'rating': persist_review.rating, 'content': persist_review.content})
        assert response.status_code == 302
        assert Review.objects.get(pk=persist_review.pk).rating == 1
        assert Review.objects.get(pk=persist_review.pk).content == "Greate course"

    def test_delete_review(self, client, persist_user, persist_review):
        client.force_login(persist_user)
        response = client.post(reverse('delete_review', args=[persist_review.pk]))
        assert response.status_code == 302
        assert not Review.objects.filter(pk=persist_review.pk).exists()

    def test_show_reviews_view(self, client, persist_user, persist_review):
        client.force_login(persist_user)
        response = client.get(reverse('reviews', args=[persist_review.course_id]))
        assert response.status_code == 200
        assert any(persist_review.pk == review.pk for review in response.context['reviews_by_course'])

    def test_show_without_reviews_view(self, client, persist_user, persist_course):
        client.force_login(persist_user)
        response = client.get(reverse('reviews', args=[persist_course.course_id]))
        assert response.status_code == 200
        assert response.context['reviews_by_course'] == []
        assert b"No reviews available" in response.content
