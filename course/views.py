from django.shortcuts import render, redirect, reverse
from course.models import Review, TeacherCourse
from course.forms import ReviewForm
from django.contrib import messages
from django.views.generic import DeleteView, UpdateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


class CourseList(LoginRequiredMixin, View):
    def get(self, request):
        courses = TeacherCourse.objects.get_teacher_courses(request.user)
        courses |= TeacherCourse.objects.get_student_approved_teacher_courses(request.user)
        context = {'courses': courses}
        return render(request, 'course/courses.html', context)


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
