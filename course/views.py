from django.shortcuts import render, redirect
from course.models import Review, TeacherCourse, StudentCourse
from course.forms import ReviewForm
from django.contrib import messages
from django.views.generic import DeleteView, UpdateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TeacherCourseForm


class CourseList(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.profile.account_type == 'B':
            teacherCourse = TeacherCourse.objects.get_teacher_courses(request.user)
            studentCourse = TeacherCourse.objects.get_student_approved_teacher_courses(request.user)
            context = {'teacher_courses': teacherCourse, 'student_courses': studentCourse}
            return render(request, 'course/courses_two_tables.html', context)
        else:
            if request.user.profile.account_type == 'T':
                courses = TeacherCourse.objects.get_teacher_courses(request.user)
            if request.user.profile.account_type == 'S':
                courses = TeacherCourse.objects.get_student_approved_teacher_courses(request.user)
            context = {'courses': courses}
            return render(request, 'course/courses_table.html', context)


class CreateReviewView(LoginRequiredMixin, CreateView):
    def post(self, request, course_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            course = TeacherCourse.objects.filter(course_id=course_id)[0]
            rating = request.POST.get('rating')
            content = request.POST.get('content')
            review = Review(student=request.user, course=course, rating=rating, content=content)
            review.save()
            return redirect('/course/' + str(course_id))
        else:
            messages.error(request, "You must enter rating")
            return redirect('/course/' + str(course_id))


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    context_object_name = 'coursePage'
    template_name = "course/course_page.html"
    fields = ['rating', 'content']

    def post(self, request, course_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = request.POST.get('rating')
            content = request.POST.get('content')
            existed_review = Review.objects.get_review_in_course_by_student(student=request.user, course=course_id)
            existed_review.rating = rating
            existed_review.content = content
            existed_review.save()
            return redirect('/course/' + str(course_id))


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    context_object_name = 'coursePage'
    template_name = "course/course_page.html"

    def post(self, request, course_id):
        review = Review.objects.get_review_in_course_by_student(request.user, course_id)
        if review:
            review.delete()
        return redirect('/course/' + str(course_id))


class AddCourse(LoginRequiredMixin, View):
    def get(self, request):
        form = TeacherCourseForm()
        context = {'form': form}
        return render(request, 'course/add_course.html', context)

    def post(self, request):
        user = TeacherCourse(teacher_id=request.user)
        form = TeacherCourseForm(request.POST, instance=user)
        form.save(request.POST)
        return redirect('show_courses')


class CoursePage(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = TeacherCourse.objects.filter(course_id=course_id)[0]
        view = course.is_student_in_course(request.user)
        reviews = Review.objects.get_reviews_by_course(course=course_id)
        review_view = Review.objects.check_if_review_exist_by_student(request.user, course)
        if review_view:
            form_view = ReviewForm(instance=review_view)
        else:
            form_view = ReviewForm()
        context = {'course': course, 'reviews': reviews, 'view': view,
                   'form': form_view, 'review_view': review_view}

        return render(request, 'course/course_page.html', context)


class ConnectCourseToStudent(LoginRequiredMixin, View):
    def post(self, request, course_id):
        course = TeacherCourse.objects.filter(course_id=course_id)[0]
        studentCourse = StudentCourse(student_id=request.user, teacher_course_id=course)
        studentCourse.save()
        return redirect('/course/' + str(course_id))
