import pytest

from django.contrib.auth.models import User

from study_group.models import StudyGroup


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
