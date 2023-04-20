from django.db import migrations, transaction


def generate_data(apps, schema_editor):
    from django.contrib.auth.models import User
    from study_group.models import StudyGroup, GroupMember

    owner1 = User.objects.create_user(username='owner1', password='password')
    owner1.save()

    owner2 = User.objects.create_user(username='owner2', password='password')
    owner2.save()

    member1 = User.objects.create_user(username='member1', password='password')
    member1.save()

    member2 = User.objects.create_user(username='member2', password='password')
    member2.save()

    groups = [
        StudyGroup(group_owner=owner1, field='Math',
                   group_description='This is a group for math enthusiasts', capacity=5),
        StudyGroup(group_owner=owner2, field='Science',
                   group_description='This is a group for science lovers', capacity=10),
        StudyGroup(group_owner=owner1, field='History',
                   group_description='This is a group for history buffs', capacity=7),
    ]

    with transaction.atomic():
        for group in groups:
            group.save()

    GroupMember(group_id=groups[0], private_id=member1).save()
    GroupMember(group_id=groups[0], private_id=member2).save()
    GroupMember(group_id=groups[1], private_id=member1).save()
    GroupMember(group_id=groups[1], private_id=member2).save()
    GroupMember(group_id=groups[2], private_id=member1).save()


class Migration(migrations.Migration):

    dependencies = [
        ('study_group', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_data),
    ]
