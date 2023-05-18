from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, PostManager
from .forms import FeedForm


class PostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'feed_page.html'
    context_object_name = 'feed'

    def get_queryset(self):
        user = self.request.user
        queryset = PostManager.get_posts_for_user(user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_form'] = FeedForm()
        context['posts'] = self.get_queryset()
        return context

    def post(self, request):
        user = request.user
        form = FeedForm(request.POST, user_id=user)
        form.save(commit=False)
        if form.is_valid():
            form.save()
        return redirect('feed_list')
