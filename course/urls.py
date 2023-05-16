from django.urls import path
from .views import CourseList

urlpatterns = [
    path('', CourseList.as_view(), name='show_courses'),
]
