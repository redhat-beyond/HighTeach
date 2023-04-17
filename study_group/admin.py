from django.contrib import admin
from .models import StudyGroup, GroupMember

# Register your models here.
admin.site.register(StudyGroup)
admin.site.register(GroupMember)
