from django.urls import path
from .views import PostsListView

urlpatterns = [
    path('list/', PostsListView.as_view(), name="feed_list"),
]
