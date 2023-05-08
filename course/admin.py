from django.contrib import admin
from course.models import StudentCourses, Review, TeacherCourses


class StudentCoursesAdmin(admin.ModelAdmin):
    list_display = ('student_course_id', 'student_id', 'teacher_course_id', 'request_date', 'status')
    list_filter = ('status',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["teacher_course_id", "student_id", 'status']
        return ['status']


class TeacherCoursesAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'teacher_id', 'course_name', 'price', 'category', 'get_experience',
                    'difficulty_level')
    list_filter = ('category', 'years_of_experience', 'difficulty_level')
    search_fields = ('course_id', 'course_name',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["teacher_id"]
        return []


admin.site.register(TeacherCourses, TeacherCoursesAdmin)
admin.site.register(StudentCourses, StudentCoursesAdmin)
admin.site.register(Review)
