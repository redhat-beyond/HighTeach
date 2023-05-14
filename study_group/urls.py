from django.urls import path
from .views import StudyGroupDetailView, StudyGroupUpdateView, LeaveJoinGroupView

urlpatterns = [
    path('detail/<int:pk>/', StudyGroupDetailView.as_view(), name="study_group_detail"),
    path('update/<int:pk>/', StudyGroupUpdateView.as_view(), name="study_group_update"),
    path('join_leave/<int:pk>/', LeaveJoinGroupView.as_view(), name="leave_or_join_group"),
]
