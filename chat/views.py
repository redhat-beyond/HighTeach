from django.shortcuts import render
from django.core.exceptions import ValidationError
from chat.models import Message
from chat.serializer import MessageSerializer
from course.models import StudentCourse
from study_group.models import StudyGroup
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


def chat_view(request):
    if request.user.profile.account_type == 'S':
        student_courses = StudentCourse.objects.get_student_courses(request.user)
    else:
        student_courses = StudentCourse.objects.get_student_courses_by_teacher(request.user)
    study_groups = StudyGroup.objects.get_groups_by_user(request.user)
    context = {
        'student_courses': student_courses,
        'study_groups': study_groups,
    }
    return render(request, 'chat/chat.html', context)


@api_view(['GET'])
def getCourseChat(request, course_id):
    course = StudentCourse.objects.get_course(course_id)[0]
    if not request.user.is_authenticated or (
            request.user != course.student_id and request.user != course.teacher_course_id.teacher_id):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    messages = Message.objects.get_student_course_chat(student_course_id=course_id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getGroupChat(request, group_id):
    group = StudyGroup.objects.get_group_by_id(group_id)[0]
    if not request.user.is_authenticated or not group.is_user_in_group(request.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    messages = Message.objects.get_group_chat(group_id=group_id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addMessage(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    course, group = None, None
    if 'courseId' in request.data:
        courses = StudentCourse.objects.get_course(int(request.data['courseId']))
        if len(courses) > 0:
            course = courses[0]
    if 'groupId' in request.data:
        groups = StudyGroup.objects.get_group_by_id(int(request.data['groupId']))
        if len(groups) > 0:
            group = groups[0]
    try:
        new_message = Message(sender=request.user, student_course=course, group=group, message=request.data['message'])
        new_message.save()
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response()
