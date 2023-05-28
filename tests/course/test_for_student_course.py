import pytest
from course.models import TeacherCourse, StudentCourse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# VALID
PENDING = 'Pending'
CONFIRMED = 'Confirmed'
COURSE_NAME = "math course"
DESCRIPTION = "this is a math course"
DIFFICULTY = 'A'
CATEGORY = "MATHS"
PRICE = 100
YEARS_OF_EXP = 3
INVALID_STATUS = 'not status'


# user 1
@pytest.fixture
def user_zero():
    return User(username="user0", password="123")


# user 2
@pytest.fixture
def user_one(db):
    user = User(username="user1", password="123")
    user.save()
    return user


# teacher 1
@pytest.fixture
def teacher_course_zero(db, user_zero):
    user_zero.save()
    return TeacherCourse(teacher_id=user_zero, course_name=COURSE_NAME, description=DESCRIPTION,
                         difficulty_level=DIFFICULTY, category=CATEGORY)


# teacher 2
@pytest.fixture
def teacher_course_one(db, user_zero):
    user_zero.save()
    teacher_course = TeacherCourse(teacher_id=user_zero, course_name=COURSE_NAME, description=DESCRIPTION,
                                   difficulty_level=DIFFICULTY, category=CATEGORY, price=PRICE,
                                   years_of_experience=YEARS_OF_EXP)
    teacher_course.save()
    return teacher_course


# teacher 3
@pytest.fixture
def teacher_course_two(db, user_one):
    teacher_course = TeacherCourse(teacher_id=user_one, course_name=COURSE_NAME, description=DESCRIPTION,
                                   difficulty_level=DIFFICULTY, category=CATEGORY, price=PRICE,
                                   years_of_experience=YEARS_OF_EXP)
    teacher_course.save()
    return teacher_course


# student 1
@pytest.fixture
def student_course_zero(teacher_course_one, user_one):
    return StudentCourse(student_id=user_one, teacher_course_id=teacher_course_one)


# student 2 / TEACHER = USER0 , STUDENT = USER1
@pytest.fixture
def student_course_one(db, teacher_course_one, user_one):
    student_course = StudentCourse(student_id=user_one, teacher_course_id=teacher_course_one)
    student_course.save()
    return student_course


# student 3 / TEACHER = USER1 , STUDENT = USER0
@pytest.fixture
def student_course_two(db, teacher_course_two, user_zero):
    user_zero.save()
    student_course = StudentCourse(student_id=user_zero, teacher_course_id=teacher_course_two)
    student_course.save()
    return student_course


class TestStudentCourse:

    def test_change_to_confirmed(self, student_course_one):
        assert student_course_one.status == PENDING
        student_course_one.change_to_confirmed()
        assert student_course_one.status == CONFIRMED

    def test_teacher_pending(self, student_course_one, student_course_two, user_zero, user_one):
        course_id1 = student_course_one.teacher_course_id.course_id
        course_id2 = student_course_two.teacher_course_id.course_id
        teacher_id1 = user_zero.pk
        teacher_id2 = user_one.pk

        assert course_id1 in StudentCourse.objects.get_teacher_pending(teacher_id1)
        assert course_id1 not in StudentCourse.objects.get_teacher_pending(teacher_id2)

        assert course_id2 not in StudentCourse.objects.get_teacher_pending(teacher_id1)
        assert course_id2 in StudentCourse.objects.get_teacher_pending(teacher_id2)

    def test_teacher_pending_with_change_to_confirmed(self, student_course_one, user_zero):
        course_id1 = student_course_one.teacher_course_id.course_id
        teacher_id1 = user_zero.pk

        assert course_id1 in StudentCourse.objects.get_teacher_pending(teacher_id1)
        student_course_one.change_to_confirmed()
        assert course_id1 not in StudentCourse.objects.get_teacher_pending(teacher_id1)

    def test_student_pending(self, student_course_one, student_course_two, user_zero, user_one):
        student_id1 = user_one
        student_id2 = user_zero

        assert student_course_one in StudentCourse.objects.get_student_pending(student_id1)
        assert student_course_one not in StudentCourse.objects.get_student_pending(student_id2)

        assert student_course_two not in StudentCourse.objects.get_student_pending(student_id1)
        assert student_course_two in StudentCourse.objects.get_student_pending(student_id2)

    def test_student_pending_with_change_to_confirmed(self, student_course_one, user_one):
        student_id1 = user_one

        assert student_course_one in StudentCourse.objects.get_student_pending(student_id1)
        student_course_one.change_to_confirmed()
        assert student_course_one not in StudentCourse.objects.get_student_pending(student_id1)

    def test_student_courses(self, student_course_one, student_course_two, user_zero, user_one):
        student_id1 = user_one
        student_id2 = user_zero

        assert student_course_one in StudentCourse.objects.get_student_courses(student_id1)
        assert student_course_two not in StudentCourse.objects.get_student_courses(student_id1)

        assert student_course_one not in StudentCourse.objects.get_student_courses(student_id2)
        assert student_course_two in StudentCourse.objects.get_student_courses(student_id2)

    def test_regitser_to_your_own_course_fails_validation(self, db, teacher_course_one, user_zero):
        with pytest.raises(ValidationError):
            student_course = StudentCourse(student_id=user_zero, teacher_course_id=teacher_course_one)
            student_course.save()

    def test_regitser_to_the_same_course_twice__fails_validation(self, db, teacher_course_one, user_one):
        with pytest.raises(ValidationError):
            student_course = StudentCourse(student_id=user_one, teacher_course_id=teacher_course_one)
            student_course.save()
            student_course1 = StudentCourse(student_id=user_one, teacher_course_id=teacher_course_one)
            student_course1.save()

    def test_invaled_status_fails_validation(self, db, teacher_course_one, user_one):
        with pytest.raises(ValidationError):
            student_course = StudentCourse(student_id=user_one, teacher_course_id=teacher_course_one,
                                           status=INVALID_STATUS)
            student_course.save()

    def test_registering_a_student_without_user_fails_validation(self, db, teacher_course_two, user_zero):
        with pytest.raises(ValidationError):
            student_course = StudentCourse(student_id=user_zero, teacher_course_id=teacher_course_two)
            student_course.save()

    def test_registering_a_student_without_teacher_course_fails_validation(self, db, teacher_course_zero, user_one):
        with pytest.raises(ValidationError):
            student_course = StudentCourse(student_id=user_one, teacher_course_id=teacher_course_zero)
            student_course.save()

    def test_get_student_courses_by_teacher(self, db, persist_course, persist_first_student_course):
        courses = StudentCourse.objects.get_student_courses_by_teacher(persist_course.teacher_id)
        assert persist_first_student_course in courses
