import pytest
import os.path
from django.conf import settings


@pytest.mark.django_db
def test_image_upload(image_file, persist_post_for_first_course):
    persist_post_for_first_course.image = image_file
    persist_post_for_first_course.save()
    media_path = os.path.join(settings.MEDIA_ROOT, str(persist_post_for_first_course.image))

    assert os.path.isfile(media_path)
