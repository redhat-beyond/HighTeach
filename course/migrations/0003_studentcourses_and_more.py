# Generated by Django 4.2 on 2023-04-20 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_alter_review_student_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentCourses',
            fields=[
                ('student_course_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')],
                                            default='Pending', max_length=30)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to=settings.AUTH_USER_MODEL)),
                ('teacher_course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                        to='course.teachercourses')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Student Courses',
            },
        ),
        migrations.AddConstraint(
            model_name='studentcourses',
            constraint=models.UniqueConstraint(fields=('student_id', 'teacher_course_id'),
                                               name='Already have a pending/confirmed request in this course'),
        ),
    ]
