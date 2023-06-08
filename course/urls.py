from django.urls import path
from .views import CourseList, AddCourse, CoursePage, ConnectCourseToStudent, AcceptOrDeclineStudentCourse
from course import views


urlpatterns = [
    path('<int:course_id>/add_review', views.CreateReviewView.as_view(), name="add_review"),
    path('<int:course_id>/delete_review', views.DeleteReviewView.as_view(), name="delete_review"),
    path('<int:course_id>/update_review', views.UpdateReviewView.as_view(), name="update_review"),
    path('', CourseList.as_view(), name='show_courses'),
    path('add', AddCourse.as_view(), name="add_course"),
    path('<int:course_id>', CoursePage.as_view(), name="coursePage"),
    path('<int:course_id>/connect', ConnectCourseToStudent.as_view(), name="connect"),
    path('<int:course_id>/<int:student_course_id>', AcceptOrDeclineStudentCourse.as_view(),
         name="accept_decline_request"),
]
