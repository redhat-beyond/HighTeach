from django.shortcuts import render
from .models import TeacherCourse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class CourseList(LoginRequiredMixin, View):
    def get(self, request):
        courses = TeacherCourse.objects.get_teacher_courses(request.user)
        courses |= TeacherCourse.objects.get_student_approved_teacher_courses(request.user)
        context = {'courses': courses}
        return render(request, 'course/courses.html', context)
