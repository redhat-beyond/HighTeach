import pytest
from course.models import TeacherCourse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError


# VALID
COURSE_NAME = "math course"
DESCRIPTION = "this is a math course"
DIFFICULTY = 'A'
CATEGORY = "MATHS"
PRICE = 100
YEARS_OF_EXP = 3

# NOT VALID
NAME_TOO_LONG = "BLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAH"
NOT_VALED_YEARS_OF_EXP = 1000
NOT_VALED_DIFFICULTY = 'kaallllll'
NOT_VALED_CATEGORY = 'KARATE'


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


class TestTeacherCourse:

    def test_price_filter(self, teacher_course_one):
        assert teacher_course_one in TeacherCourse.objects.in_price_range(PRICE-1, PRICE+1)
        assert teacher_course_one not in TeacherCourse.objects.in_price_range(PRICE+1, PRICE+2)
        assert teacher_course_one not in TeacherCourse.objects.in_price_range(PRICE-1, PRICE-2)
        assert teacher_course_one in TeacherCourse.objects.in_price_range(PRICE, PRICE)

    def test_category_filter(self, teacher_course_one):
        assert teacher_course_one in TeacherCourse.objects.in_category(CATEGORY)
        assert teacher_course_one not in TeacherCourse.objects.in_category(CATEGORY + "not a category")

    def test_experience_filter(self, teacher_course_one):
        assert teacher_course_one in TeacherCourse.objects.got_experience(YEARS_OF_EXP)
        assert teacher_course_one in TeacherCourse.objects.got_experience(YEARS_OF_EXP - 1)
        assert teacher_course_one not in TeacherCourse.objects.got_experience(YEARS_OF_EXP + 1)

    def test_search_name_filter(self, teacher_course_one):
        assert teacher_course_one in TeacherCourse.objects.search_name(COURSE_NAME)
        assert teacher_course_one in TeacherCourse.objects.search_name(DESCRIPTION)
        assert teacher_course_one in TeacherCourse.objects.search_name(COURSE_NAME[:2])
        assert teacher_course_one in TeacherCourse.objects.search_name(DESCRIPTION[:2])
        assert teacher_course_one not in TeacherCourse.objects.search_name("not a course name or description")

    def test_difficulty_level_filter(self, teacher_course_one):
        assert teacher_course_one in TeacherCourse.objects.get_level(DIFFICULTY)
        assert teacher_course_one not in TeacherCourse.objects.get_level('B')

    def test_get_teacher_courses_filter(self, teacher_course_one, teacher_course_two):
        teacher_id1 = teacher_course_one.teacher_id.pk
        teacher_id2 = teacher_course_two.teacher_id.pk

        assert teacher_course_one in TeacherCourse.objects.get_teacher_courses(teacher_id1)
        assert teacher_id1 != teacher_id2
        assert teacher_course_one not in TeacherCourse.objects.get_teacher_courses(teacher_id2)

    def test_course_name_too_long_fails_validation(self, db, teacher_course_zero):
        with pytest.raises(ValidationError):
            teacher_course_zero.course_name = NAME_TOO_LONG
            teacher_course_zero.save()

    def test_course_name_empty_fails_validation(self, db, user_one):
        with pytest.raises(ValidationError):
            teacher_course = TeacherCourse(teacher_id=user_one, description=DESCRIPTION,
                                           difficulty_level=DIFFICULTY, category=CATEGORY, price=PRICE,
                                           years_of_experience=YEARS_OF_EXP)
            teacher_course.save()

    def test_price_negative_amount_fails_validation(self, db, teacher_course_zero):
        with pytest.raises(IntegrityError):
            teacher_course_zero.price = -PRICE
            teacher_course_zero.save()

    def test_years_of_experience_negative_amount_fails_validation(self, db, teacher_course_zero):
        with pytest.raises(ValidationError):
            teacher_course_zero.years_of_experience = -YEARS_OF_EXP
            teacher_course_zero.save()

    def test_years_of_experience_invaled_fails_validation(self, db, teacher_course_zero):
        with pytest.raises(ValidationError):
            teacher_course_zero.years_of_experience = NOT_VALED_YEARS_OF_EXP
            teacher_course_zero.save()

    def test_difficulty_level_invaled_choice_fails_validation(self, db, teacher_course_zero):
        with pytest.raises(ValidationError):
            teacher_course_zero.difficulty_level = NOT_VALED_DIFFICULTY
            teacher_course_zero.save()

    def test_difficulty_level_empty_fails_validation(self, db, user_one):
        with pytest.raises(ValidationError):
            teacher_course = TeacherCourse(teacher_id=user_one, course_name=COURSE_NAME, description=DESCRIPTION,
                                           category=CATEGORY, price=PRICE, years_of_experience=YEARS_OF_EXP)
            teacher_course.save()

    def test_category_invaled_choice_fails_validation(self, db, teacher_course_zero):
        with pytest.raises(ValidationError):
            teacher_course_zero.category = NOT_VALED_CATEGORY
            teacher_course_zero.save()

    def test_category_empty_fails_validation(self, db, user_one):
        with pytest.raises(ValidationError):
            teacher_course = TeacherCourse(teacher_id=user_one, course_name=COURSE_NAME, description=DESCRIPTION,
                                           difficulty_level=DIFFICULTY, price=PRICE, years_of_experience=YEARS_OF_EXP)
            teacher_course.save()

    def test_teacher_id_empty_fails_validation(self, db, user_zero):
        with pytest.raises(ValidationError):
            teacher_course = TeacherCourse(teacher_id=user_zero, course_name=COURSE_NAME, description=DESCRIPTION,
                                           difficulty_level=DIFFICULTY, price=PRICE, years_of_experience=YEARS_OF_EXP)
            teacher_course.save()
