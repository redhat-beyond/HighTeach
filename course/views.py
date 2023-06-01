from django.shortcuts import render, redirect, reverse
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
    def get(self, request, course_id):
        form_view = ReviewForm()
        return render(request, 'course/create_review.html', {'form': form_view, 'course_id': course_id})

    def post(self, request, course_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            course = TeacherCourse.objects.filter(course_id=course_id)[0]
            rating = request.POST.get('rating')
            content = request.POST.get('content')
            review = Review(student=request.user,  course=course, rating=rating, content=content)
            review.save()
            return redirect(reverse('reviews', args=[course_id]))
        else:
            messages.error(request, "You must enter rating")
            return render(request, 'course/create_review.html', {'form': form, 'course_id': course_id})


class ShowReviews(LoginRequiredMixin, View):
    def get(self, request, course_id):
        reviews = Review.objects.get_reviews_by_course(course_id)
        if reviews:
            return render(request, "course/reviews_by_course.html", {'reviews_by_course': reviews})
        else:
            return render(request, "course/reviews_by_course.html", {'reviews_by_course': []})


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    context_object_name = 'reviews'
    template_name = "course/create_review.html"
    fields = ['rating', 'content']

    def get_success_url(self):
        return reverse('reviews', kwargs={'course_id': self.object.course_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.object.course_id
        return context


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    context_object_name = 'reviews'
    template_name = "course/reviews_by_course.html"

    def get_success_url(self):
        return reverse('reviews', kwargs={'course_id': self.object.course_id})


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
        context = {'course': course, 'reviews': reviews, 'view': view}
        return render(request, 'course/course_page.html', context)


class ConnectCourseToStudent(LoginRequiredMixin, View):
    def post(self, request, course_id):
        course = TeacherCourse.objects.filter(course_id=course_id)[0]
        studentCourse = StudentCourse(student_id=request.user, teacher_course_id=course)
        studentCourse.save()
        return redirect('/course/' + str(course_id))
