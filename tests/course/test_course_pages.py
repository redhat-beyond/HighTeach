import pytest
from course.models import TeacherCourse, StudentCourse
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


@pytest.mark.django_db
class TestCourseTableView:

    def test_courses_list_authorized_student_or_teacher(self, authorized_client_teacher):
        course_response = authorized_client_teacher.get('/course/')
        assert course_response.status_code == 200
        assert 'courses_table.html' in course_response.templates[0].name

    def test_courses_list_authorized_student_and_teacher(self, authorized_client_teacher_and_student):
        course_response = authorized_client_teacher_and_student.get('/course/')
        assert course_response.status_code == 200
        assert 'courses_two_tables.html' in course_response.templates[0].name

    def test_courses_list_unauthorized(self, client):
        course_response = client.get('/course/')
        assert course_response.status_code == 302

    def test_show_course_that_user_teaches(self, authorized_client_teacher, teacher_course_zero):
        response = authorized_client_teacher.get(reverse('show_courses'))
        assert response.status_code == 200
        courses_ids = [course.pk for course in response.context['courses']]
        assert teacher_course_zero.course_id in courses_ids

    def test_show_course_that_user_enrolled_in(self, authorized_client_teacher_and_student,
                                               persist_first_student_course):
        response = authorized_client_teacher_and_student.get(reverse('show_courses'))
        assert response.status_code == 200
        courses_ids = [course.pk for course in response.context['student_courses']]
        assert persist_first_student_course.student_course_id in courses_ids


@pytest.mark.django_db
class TestAddCourseView:

    def test_courses_add_authorized(self, authorized_client):
        course_response = authorized_client.get('/course/add')
        assert course_response.status_code == 200
        assert 'add_course.html' in course_response.templates[0].name

    def test_courses_add_unauthorized(self, client):
        course_response = client.get('/course/add')
        assert course_response.status_code == 302

    def test_add_course(self, authorized_client_teacher):
        teacher_course = {"course_name": COURSE_NAME, "description": DESCRIPTION,
                          "difficulty_level": DIFFICULTY, "category": CATEGORY,
                          "price": PRICE, "years_of_experience": YEARS_OF_EXP}
        assert not TeacherCourse.objects.filter(**teacher_course).exists()
        course_creation_response = authorized_client_teacher.post("/course/add", teacher_course, follow=True)
        assert course_creation_response.status_code == 200
        assert 'courses_table.html' in course_creation_response.templates[0].name
        assert TeacherCourse.objects.filter(**teacher_course).exists()


@pytest.mark.django_db
class TestCoursePageView:

    def test_coures_page_authorized(self, authorized_client, persist_course):
        course_response = authorized_client.get('/course/' + str(persist_course.course_id))
        assert course_response.status_code == 200
        expected_template_name = 'course_page.html'
        page_templates = course_response.templates[0].name
        assert expected_template_name in page_templates

    def test_courses_page_unauthorized(self, client, persist_course):
        course_response = client.get('/course/' + str(persist_course.course_id))
        assert course_response.status_code == 302

    def test_enroll_in_course(self, authorized_client, persist_course, persist_user):
        student_course = {'teacher_course_id': persist_course, 'student_id': persist_user}
        assert not StudentCourse.objects.filter(**student_course).exists()
        course_creation_response = authorized_client.post("/course/" + str(persist_course.course_id) + "/connect",
                                                          follow=True)
        assert course_creation_response.status_code == 200
        assert StudentCourse.objects.filter(**student_course).exists()
        expected_template_name = 'course_page.html'
        page_templates = course_creation_response.templates[0].name
        assert expected_template_name in page_templates

    def test_show_course_page(self, authorized_client, persist_course):
        response = authorized_client.get("/course/" + str(persist_course.course_id))
        assert response.status_code == 200
        course_in_page = response.context['course']
        assert persist_course.course_id == course_in_page.course_id
