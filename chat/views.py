from django.shortcuts import render
from chat.models import ChatManager, Message
from chat.serializer import MessageSerializer
from course.models import StudentCourse
from study_group.models import StudyGroup
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
def chat_view(request):
    if request.user.profile.account_type == 'S':
        student_courses = ChatManager.get_student_contacts_list(request.user)
    else:
        student_courses = ChatManager.get_teacher_contacts_list(request.user)
    study_groups = StudyGroup.objects.get_groups_by_user(request.user)
    context = {
        'student_courses': student_courses,
        'study_groups': study_groups,
    }
    return render(request, 'chat/chat.html', context)


@api_view(['GET'])
def getCourseChat(request, course_id):
    messages = Message.objects.get_student_course_chat(student_course_id=course_id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getGroupChat(request, group_id):
    messages = Message.objects.get_group_chat(group_id=group_id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addMessage(request):
    if 'courseId' in request.data:
        course = StudentCourse.objects.get_course(int(request.data['courseId']))[0]
    else:
        course = None
    if 'groupId' in request.data:
        group = StudyGroup.objects.get_group_by_id(int(request.data['groupId']))[0]
    else:
        group = None

    new_message = Message(sender=request.user, student_course=course, group=group, message=request.data['message'])
    new_message.save()
    return Response()
