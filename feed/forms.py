from django import forms
from .models import Post


class FeedForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_id', 'content', 'course_id')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_id', None)
        self.user_id = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        new_post = super().save(commit=False)
        new_post.user_id = self.user_id
        if commit:
            new_post.save()

        return new_post
