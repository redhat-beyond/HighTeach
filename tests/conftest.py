import pytest

from django.contrib.auth.models import User
from study_group.models import StudyGroup
from course.models import StudentCourses, TeacherCourses
from chat.models import Message


@pytest.fixture
def new_user():
    user = User(username="test1",
                first_name="test",
                last_name="mctest",
                email="test123@gmail.com")

    user.set_password("PASSWORD")
    return user


@pytest.fixture
def new_second_user():
    user = User(username='second_user',
                first_name='second',
                last_name='user',
                email='email@gmail.com')

    user.set_password('second_pass')
    return user


@pytest.fixture
def persist_user(new_user):
    new_user.save()
    return new_user


@pytest.fixture
def persist_second_user(new_second_user):
    new_second_user.save()
    return new_second_user


@pytest.fixture
def new_group(persist_user):
    group = StudyGroup(group_owner=persist_user,
                       field="CS group fixture",
                       group_description="high school level CS",
                       capacity=2)
    return group


@pytest.fixture
def new_second_group(persist_second_user):
    group = StudyGroup(group_owner=persist_second_user,
                       field="guitar playing group fixture",
                       group_description="learning guitar for beginners",
                       capacity=5)
    return group


@pytest.fixture
def persist_group(new_group):
    new_group.save()
    return new_group


@pytest.fixture
def persist_second_group(new_second_group):
    new_second_group.save()
    return new_second_group


@pytest.fixture
def persist_set(persist_group):
    return [persist_group]


@pytest.fixture
def user_without_group_and_course():
    user = User(username="user_without_group_and_course",
                first_name="user_without_group_and_course",
                last_name="user_without_group_and_course",
                email="user_without_group_and_course@gmail.com")

    user.set_password("PASSWORD")
    user.save()
    return user


@pytest.fixture
def study_group0(persist_user):
    group = StudyGroup(group_owner=persist_user,
                       field="math group",
                       group_description="high school level math",
                       capacity=2)
    group.save()
    group.join_group(persist_user)
    return group


@pytest.fixture
def student_course0(persist_user, persist_second_user):
    teacher_course1 = TeacherCourses(teacher_id=persist_user, price=5, description='Test', course_name='Test Math',
                                     difficulty_level='B', category='MATHS')
    teacher_course1.save()
    student_course = StudentCourses(student_id=persist_second_user, teacher_course_id=teacher_course1)
    student_course.save()
    return student_course


_TEST_MESSAGE = "Test message"


@pytest.fixture
def message_with_group(persist_user, study_group0):
    return Message(sender=persist_user, group=study_group0, message=_TEST_MESSAGE)


@pytest.fixture
def message_with_student_course(persist_user, student_course0):
    return Message(sender=persist_user, student_course=student_course0, message=_TEST_MESSAGE)
