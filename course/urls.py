from django.urls import path
from .views import CourseList
from course import views


urlpatterns = [
    path('review/<int:course_id>/create_review', views.CreateReviewView.as_view(), name="create_review"),
    path('review/<int:course_id>', views.ShowReviews.as_view(), name='reviews'),
    path('review/delete_review/<int:pk>/', views.DeleteReviewView.as_view(), name="delete_review"),
    path('review/update_review/<int:pk>/', views.UpdateReviewView.as_view(), name="update_review"),
    path('', CourseList.as_view(), name='show_courses'),
]
