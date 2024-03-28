from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, PostVideo, Comment
from .forms import SearchForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SubscriptionRequiredMixin
from django.contrib import messages


class CategoryView(View):
    form_class = SearchForm

    def get(self, request):
        categories = Category.objects.all()
        if request.GET.get('search'):
            categories = Category.objects.filter(name__contains=request.GET.get('search'))
            return render(request, 'post/category.html', {'categories': categories, 'form': self.form_class})
        return render(request, 'post/category.html', {'categories': categories, 'form': self.form_class})


class PostDetailView(LoginRequiredMixin, SubscriptionRequiredMixin, View):
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.post_obj =get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_obj
        videos = PostVideo.objects.filter(post=post)
        comments = post.p_comments.all()
        same_posts = Post.objects.filter(category=post.category)
        return render(request, 'post/post-detail.html', {'post': post,
                                                         'videos': videos,
                                                         'comments': comments,
                                                         'form': self.form_class,
                                                         'same_posts': same_posts})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            complete_comment = form.save(commit=False)
            complete_comment.user = request.user
            complete_comment.post = self.post_obj
            complete_comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد', 'success')
            return redirect('post:detail', self.post_obj.id)
        return render(request, 'post/post-detail.html', {'form': self.form_class})


class PostsOfCategory(View):
    def get(self, request, category_id):
        posts = Post.objects.filter(category=category_id)
        post_category_name = posts.category.name
        return render(request, 'post/posts-of-category.html', {'posts': posts,
                                                               'post_category_name': post_category_name})


class SearchInHomeView(View):
    def get(self, request):
        search = request.GET.get('term')
        posts = Post.objects.all()

        if search:
            posts = posts.filter(category__name__contains=search)

        return render(request, 'home/home.html', {'posts': posts})