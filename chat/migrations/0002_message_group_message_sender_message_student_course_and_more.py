# Generated by Django 4.2 on 2023-04-24 21:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study_group', '0002_test_data'),
        ('course', '0003_studentcourses_and_more'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='study_group.studygroup'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='student_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='course.studentcourses'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.BigAutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddConstraint(
            model_name='message',
            constraint=models.CheckConstraint(
                check=models.Q(models.Q(('group__isnull', False), ('student_course__isnull', True)),
                               models.Q(('group__isnull', True), ('student_course__isnull', False)), _connector='OR'),
                name='chats_messages_student_course_or_study_group'),
        ),
    ]
