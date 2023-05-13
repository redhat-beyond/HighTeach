from django import forms
from .models import StudyGroup


class StudyGroupCreationForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['field', 'group_description', 'capacity']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('group_owner', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        new_study_group = super().save(commit=False)
        new_study_group.group_owner = self.user

        if commit:
            new_study_group.save()

        new_study_group.join_group(self.user)
        return new_study_group
