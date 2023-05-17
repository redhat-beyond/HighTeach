from django.views.generic import DetailView, View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

from .models import StudyGroup


class StudyGroupDetailView(LoginRequiredMixin, DetailView):
    model = StudyGroup
    template_name = "study_group_detail.html"
    context_object_name = "study_group"


class StudyGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = StudyGroup
    fields = ["field", "group_description"]
    template_name = "study_group_update.html"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().group_owner != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("study_group_detail", kwargs={"pk": self.object.pk})


class LeaveJoinGroupView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(StudyGroup, pk=pk)
        user = request.user

        if user in group.get_all_group_members():
            group.leave_group(user)
        else:
            group.join_group(user)

        return redirect('study_group_detail', pk)
