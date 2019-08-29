from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Article
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from users.models import CustomUser


# Create your views here.

class MyArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'my_articles.html'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'body',]
    template_name = 'article_edit.html'
    login_url = 'login'

    def form_valid(self, form):
        user = CustomUser.objects.get(username=self.request.user)
        if self.request.user != self.object.author and not user.is_superuser:
            return redirect(reverse('home'))
        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def form_valid(self, form):
        user = CustomUser.objects.get(username=self.request.user)
        if self.request.user != self.object.author and not user.is_superuser:
            return redirect(reverse('home'))
        return super().form_valid(form)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ['title', 'body', ]
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


