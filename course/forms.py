from django import forms
from django.forms import ModelForm
from .models import TeacherCourse


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        label='Rating:',
        choices=(
            ('5', '5 Stars'),
            ('4', '4 Stars'),
            ('3', '3 Stars'),
            ('2', '2 Stars'),
            ('1', '1 Star'),
        ),
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
    )
    content = forms.CharField(
        label='Content:',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'resize: none'}),
    )


class TeacherCourseForm(ModelForm):
    class Meta:
        model = TeacherCourse
        fields = ('course_name', 'description',
                  'price', 'years_of_experience', 'difficulty_level',
                  'category')
