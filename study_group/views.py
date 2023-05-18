from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

from .models import StudyGroup
from .forms import StudyGroupCreationForm


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


class StudyGroupListView(LoginRequiredMixin, ListView):
    model = StudyGroup
    template_name = 'study_group_hub.html'
    context_object_name = 'study_groups'

    def get_queryset(self):
        user = self.request.user
        queryset = StudyGroup.objects.get_groups_by_user(user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_study_group_form'] = StudyGroupCreationForm()
        return context

    def post(self, request):
        user = request.user
        form = StudyGroupCreationForm(request.POST, group_owner=user)
        if form.is_valid():
            form.save()
        return redirect('study_groups_list_for_user')


class LeaveJoinGroupView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(StudyGroup, pk=pk)
        user = request.user

        if user in group.get_all_group_members():
            group.leave_group(user)
        else:
            group.join_group(user)

        return redirect("study_groups_list_for_user")
