import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from study_group.models import StudyGroup
from course.models import StudentCourse, TeacherCourse, Review
from chat.models import Message
from feed.models import Post
from users.models import Profile
from datetime import date

USERNAME = "test1"
PASSWORD = "PASSWORD"
INVALID_USERNAME = "invaliduser"
INVALID_PASSWORD = "invalidpassword"


@pytest.fixture
def new_user():
    user = User(username=USERNAME,
                first_name="test",
                last_name="mctest",
                email="test123@gmail.com")

    user.set_password(PASSWORD)
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
def persist_user_profile(persist_user):
    profile = Profile.objects.create(user=persist_user)
    profile.save()
    return profile


@pytest.fixture
def persist_second_user_profile(persist_second_user):
    profile = Profile.objects.create(user=persist_second_user)
    profile.save()
    return profile


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
    teacher_course1 = TeacherCourse(teacher_id=persist_user, price=5, description='Test', course_name='Test Math',
                                    difficulty_level='B', category='MATHS')
    teacher_course1.save()
    student_course = StudentCourse(student_id=persist_second_user, teacher_course_id=teacher_course1)
    student_course.save()
    return student_course


_TEST_MESSAGE = "Test message"


@pytest.fixture
def message_with_group(persist_user, study_group0):
    return Message(sender=persist_user, group=study_group0, message=_TEST_MESSAGE)


@pytest.fixture
def persist_message_with_group(message_with_group):
    message_with_group.save()
    return message_with_group


@pytest.fixture
def message_with_student_course(persist_user, student_course0):
    return Message(sender=persist_user, student_course=student_course0, message=_TEST_MESSAGE)


@pytest.fixture
def persist_message_with_student_course(message_with_student_course):
    message_with_student_course.save()
    return message_with_student_course


@pytest.fixture
def persist_teacher():
    user = User(username="teacher1",
                first_name="test",
                last_name="mctest",
                email="test123@gmail.com")

    user.set_password("PASSWORD")
    user.save()

    return user


@pytest.fixture
def persist_second_teacher():
    user = User(username='second_teacher',
                first_name='teacher',
                last_name='mcteacher',
                email='email@gmail.com')

    user.set_password('second_pass')
    user.save()
    return user


@pytest.fixture
def persist_course(persist_teacher):
    course = TeacherCourse(teacher_id=persist_teacher,
                           course_name="linear algebra",
                           description="linear algebra for CS students",
                           price=100,
                           years_of_experience=4,
                           difficulty_level="I",
                           category="MATHS")

    course.save()
    return course


@pytest.fixture
def persist_second_course(persist_second_teacher):
    course = TeacherCourse(teacher_id=persist_second_teacher,
                           course_name="riding a tricycle",
                           description="riding a tricycle course for advanced tricycle riders",
                           price=200,
                           years_of_experience=5,
                           difficulty_level="A",
                           category="SPORT_AND_LEISURE")
    course.save()
    return course


@pytest.fixture
def persist_first_student_course(persist_course, persist_user):
    student_course = StudentCourse(student_id=persist_user,
                                   teacher_course_id=persist_course,
                                   status="Confirmed")
    student_course.save()
    return student_course


@pytest.fixture
def persist_second_student_course(persist_second_course, persist_second_user):
    student_course = StudentCourse(student_id=persist_second_user,
                                   teacher_course_id=persist_second_course,
                                   status="Confirmed")
    student_course.save()
    return student_course


@pytest.fixture
def persist_post_for_first_course(persist_course, persist_user, persist_first_student_course):
    post = Post(course_id=persist_course,
                user_id=persist_user,
                parent_post_id=None,
                content="this is a root post by a student for first course")
    post.save()
    return post


@pytest.fixture
def image_file():
    image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    return image


@pytest.fixture
def make_study_group_of_varied_size():
    def _make_study_group_of_varied_size(group_members_num, max_capacity):
        new_group = StudyGroup(
            group_owner=User.objects.create(username='group_owner', password='pass'),
            field="field",
            group_description="description",
            capacity=max_capacity)
        new_group.save()
        for i in range(group_members_num):
            new_group.join_group((User.objects.create(username=f'user{i}', password='pass')))
        return new_group

    return _make_study_group_of_varied_size


@pytest.fixture
def new_review(persist_second_user, persist_course):
    review = Review(student=persist_second_user, course=persist_course,
                    rating=1, content="Greate course", date=date(2023, 4, 17))
    return review


@pytest.fixture
def new_review_two(persist_user, persist_course):
    review = Review(student=persist_user, course=persist_course,
                    rating=2, content="Greate course", date=date(2023, 4, 17))
    return review


@pytest.fixture
def persist_review(new_review):
    new_review.save()
    return new_review


@pytest.fixture
def persist_review_number_two(new_review_two):
    new_review_two.save()
    return new_review_two


@pytest.fixture
def authorized_client(client, persist_user):
    client.force_login(persist_user)
    return client


@pytest.fixture
def add_message_to_course_request_data(student_course0):
    return {
        "courseId": student_course0.student_course_id,
        "message": "Test",
    }


@pytest.fixture
def add_message_to_group_request_data(study_group0):
    return {
        "groupId": study_group0.study_group_id,
        "message": "Test",
    }
