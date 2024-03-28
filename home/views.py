from django.shortcuts import render
from django.views import View
from accounts.models import User
from post.models import Post
from post.forms import SearchForm


class HomeView(View):
    form_class = SearchForm

    def get(self, request):
        posts = Post.objects.all()
        form = self.form_class
        if request.GET.get('search'):
            posts = posts.filter(title__contains=request.GET.get('search'))
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            return render(request, 'home/home.html', {'user': user, 'posts': posts,
                                                      'form': form})
        return render(request, 'home/home.html', {'posts': posts, 'form': form})