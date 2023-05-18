import pytest
import time

from django.core.exceptions import ValidationError

from course.models import StudentCourse
from feed.models import Post, PostManager


@pytest.fixture
def persist_reply_for_first_course(persist_course, persist_teacher,
                                   persist_post_for_first_course, persist_second_student_course):
    post = Post(course_id=persist_course,
                user_id=persist_teacher,
                parent_post_id=persist_post_for_first_course,
                content="this is a reply post by a teacher for message in first course")
    post.save()
    return post


@pytest.fixture
def persist_post_for_second_course_student(persist_second_course, persist_second_user):
    post = Post(course_id=persist_second_course,
                user_id=persist_second_user,
                parent_post_id=None,
                content="this is a root post by a second student for second course")
    post.save()
    return post


@pytest.mark.django_db
class TestPost:
    def test_is_root_post(self, persist_post_for_first_course, persist_reply_for_first_course):
        assert persist_post_for_first_course.is_root_post()
        assert not persist_reply_for_first_course.is_root_post()

    def test_post_is_only_reply_to_root_post(self, persist_user, persist_course,
                                             persist_reply_for_first_course):
        reply_to_reply = Post(course_id=persist_course, user_id=persist_user,
                              parent_post_id=persist_reply_for_first_course, content="should be invalid")
        with pytest.raises(ValidationError):
            reply_to_reply.save()

    def test_is_user_able_to_post_in_course(self, persist_user, persist_course):
        assert not Post.is_user_able_to_post_in_course(persist_user, persist_course)
        user_joined_group = StudentCourse(student_id=persist_user, teacher_course_id=persist_course,
                                          status="Confirmed")
        user_joined_group.save()
        assert Post.is_user_able_to_post_in_course(persist_user, persist_course)

    def create_post_for_user_not_related_to_course(self, persist_user, persist_course):
        assert not Post.is_user_able_to_post_in_course(persist_user, persist_course)
        invalid_post = Post(course_id=persist_course, user_id=persist_user, content="should be invalid")
        with pytest.raises(ValidationError):
            invalid_post.save()


@pytest.mark.django_db
class TestPostManager:
    def test_get_post_for_user(self, persist_user,
                               persist_first_student_course, persist_second_student_course,
                               persist_post_for_first_course, persist_reply_for_first_course,
                               persist_post_for_second_course_student):
        expected = {persist_post_for_first_course: [persist_reply_for_first_course]}
        posts_user = PostManager.get_posts_for_user(persist_user)

        assert posts_user == expected
        assert persist_post_for_second_course_student not in expected.items()

    @pytest.mark.parametrize("num_of_posts", [4])
    def test_posts_order_in_dict_by_creation_date(self, num_of_posts, persist_user, persist_course,
                                                  persist_first_student_course):
        for i in range(num_of_posts):
            time.sleep(1)
            post = Post(course_id=persist_course, user_id=persist_user, content=f"post num {i}")
            post.save()

        posts_for_user = list(PostManager.get_posts_for_user(persist_user).keys())
        assert all(earlier.date <= later.date for earlier, later in zip(posts_for_user, posts_for_user[1:]))


@pytest.mark.django_db
class TestPostsListView:
    def test_create_post(self, client, persist_course, persist_user, persist_first_student_course):
        client.force_login(persist_user)
        post_creation_form_args = {
            "course_id": persist_course.course_id,
            "user_id": persist_user,
            "content": "yarden"
        }
        assert not Post.objects.filter(**post_creation_form_args).exists()
        post_creation_response = client.post("/feed/list/", data=post_creation_form_args)
        assert post_creation_response.status_code == 302
        assert Post.objects.filter(**post_creation_form_args).exists()

    def test_created_post_in_view(self, client, persist_post_for_first_course):
        client.force_login(persist_post_for_first_course.user_id)
        response = client.get('/feed/list/')
        assert response.status_code == 200
        response_posts = response.context['posts']
        assert any(persist_post_for_first_course.post_id == post.post_id for post in response_posts)
