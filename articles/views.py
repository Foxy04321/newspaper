from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Article, Comment
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from users.models import CustomUser
from .forms import CommentForm


# Create your views here.

class MyArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'my_articles.html'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_new.html'
    fields = ['comment',]
    login_url = 'login'


    def form_valid(self, form):
        article_id = self.kwargs.get('pk', None)
        self.success_url = reverse_lazy('article_detail', args=[article_id])
        form.instance.author = self.request.user
        form.instance.article = Article.objects.get(id=article_id)
        form.save()
        return super().form_valid(form)

''' # Способ реализации добавления комментов без view
def CreateComment(request, pk):
    comment = Comment.objects.filter(article=pk)
    article = get_object_or_404(Article, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.article = article
            form.save()
            return redirect(CreateComment, pk)
    else:
        form = CommentForm()
    return render(request, 'comment_new.html',
                  {
                      'article': article,
                      'comments': comment,
                      'form': form,
                  })
'''

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


