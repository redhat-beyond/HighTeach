import pytest
from course.models import TeacherCourse
from django.urls import reverse

COURSE_NAME = "math course"
DESCRIPTION = "this is a math course"
DIFFICULTY = 'A'
CATEGORY = "MATHS"
PRICE = 100
YEARS_OF_EXP = 3


@pytest.fixture
def teacher_course_zero(persist_user):
    teacher_course = TeacherCourse(teacher_id=persist_user, course_name=COURSE_NAME, description=DESCRIPTION,
                                   difficulty_level=DIFFICULTY, category=CATEGORY, price=PRICE,
                                   years_of_experience=YEARS_OF_EXP)
    teacher_course.save()
    return teacher_course


@pytest.fixture
def authorized_client(client, persist_user):
    client.force_login(persist_user)
    return client


@pytest.mark.django_db
class TestCourseTableView:

    def test_courses_list_authorized(self, authorized_client):
        course_response = authorized_client.get('/course/')
        assert course_response.status_code == 200
        assert 'courses.html' in course_response.templates[0].name

    def test_courses_list_unauthorized(self, client):
        course_response = client.get('/course/')
        assert course_response.status_code == 302

    def test_show_course_that_user_teaches(self, authorized_client, teacher_course_zero):
        response = authorized_client.get(reverse('show_courses'))
        assert response.status_code == 200
        courses_ids = [course.pk for course in response.context['courses']]
        assert teacher_course_zero.course_id in courses_ids

    def test_show_course_that_user_enrolled_in(self, authorized_client, persist_first_student_course):
        response = authorized_client.get(reverse('show_courses'))
        assert response.status_code == 200
        courses_ids = [course.pk for course in response.context['courses']]
        assert persist_first_student_course.student_course_id in courses_ids
