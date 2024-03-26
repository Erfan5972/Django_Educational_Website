from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Category, Post, PostVideo
from .forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SubscriptionRequiredMixin


class CategoryView(View):
    form_class = SearchForm

    def get(self, request):
        categories = Category.objects.all()
        if request.GET.get('search'):
            categories = Category.objects.filter(name__contains=request.GET.get('search'))
            return render(request, 'post/category.html', {'categories': categories, 'form': self.form_class})
        return render(request, 'post/category.html', {'categories': categories, 'form': self.form_class})


class PostDetailView(LoginRequiredMixin, SubscriptionRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        videos = PostVideo.objects.filter(post=post)
        return render(request, 'post/post-detail.html', {'post': post,
                                                         'videos': videos})


class PostsOfCategory(View):
    def get(self, request, category_id):
        posts = Post.objects.filter(category=category_id)
        return render(request, 'post/posts-of-category.html', {'posts': posts})