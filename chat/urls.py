from django.urls import path
from chat import views


urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('courses/<int:course_id>', views.getCourseChat),
    path('groups/<int:group_id>', views.getGroupChat),
    path('post-message/', views.addMessage),
]
