from django import forms
from django.forms import ModelForm
from .models import TeacherCourse, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'star-rating'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'resize: none'}),
        }


class TeacherCourseForm(ModelForm):
    class Meta:
        model = TeacherCourse
        fields = ('course_name', 'description',
                  'price', 'years_of_experience', 'difficulty_level',
                  'category')
