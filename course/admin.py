from django.contrib import admin
from course.models import TeacherCourses, Review


class TeacherCoursesAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'teacher_id', 'course_name', 'price', 'category', 'get_experience',
                    'difficulty_level')
    list_filter = ('category', 'years_of_experience', 'difficulty_level')
    search_fields = ('course_id', 'course_name',)


admin.site.register(TeacherCourses, TeacherCoursesAdmin)

admin.site.register(Review)
