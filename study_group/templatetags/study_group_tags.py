from django import template

register = template.Library()


@register.filter(name='group_members_count_formatted')
def group_members_count_formatted(study_group):
    return f"{study_group.members_count}/{study_group.capacity} Members"
