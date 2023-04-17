from django.db import models
from django.db.models import Q

from django.contrib.auth.models import User


class GroupManager(models.Manager):
    def get_all_non_full_groups(self):
        return self.annotate(members_count=models.Count("group_members")) \
            .filter(members_count__lt=models.F('capacity'))

    def search_group_by_keyword(self, keyword: str):
        return self.filter(Q(group_description__icontains=keyword) | Q(field__icontains=keyword))


class StudyGroup(models.Model):
    study_group_id = models.AutoField(primary_key=True)
    group_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.CharField(max_length=30)
    group_description = models.TextField()
    capacity = models.PositiveIntegerField()
    objects = GroupManager()

    def join_group(self, user: User):
        if self.is_group_full():
            raise ValueError("Group is already full")
        if self.is_user_in_group(user):
            raise ValueError("User already in group")
        group_member = GroupMember(group_id=self, private_id=user)
        group_member.save()

    def is_group_full(self):
        return self.group_members.count() >= self.capacity

    def get_all_group_members(self):
        return User.objects.filter(pk__in=self.group_members.values_list('private_id', flat=True))

    def is_user_in_group(self, user: User):
        return self.group_members.filter(private_id=user.pk).exists()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Group: {self.field} -- Owner: {self.group_owner}"


class GroupMember(models.Model):
    group_id = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='group_members')
    private_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group: {self.group_id.field} -- Owner: {self.private_id}"
