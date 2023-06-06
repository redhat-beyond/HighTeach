from django.urls import path
from .views import ProfileDetailView, edit_profile

urlpatterns = [
    path('<str:slug>/',  ProfileDetailView.as_view(), name='profile-detail'),
    path('<str:slug>/edit-profile/', edit_profile, name='users-edit-profile'),
]
