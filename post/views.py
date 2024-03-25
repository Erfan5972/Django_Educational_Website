from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from .forms import SearchForm
from django.contrib import messages


class CategoryView(View):
    form_class = SearchForm

    def get(self, request):
        categories = Category.objects.all()
        if request.GET.get('search'):
            categories = Category.objects.filter(name__contains=request.GET.get('search'))
            return render(request, 'post/category.html', {'categories': categories, 'form': self.form_class})
        return render(request, 'post/category.html', {'categories': categories, 'form': self.form_class})


class PostDetailView(View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'post/post-detail.html', {'post': post})