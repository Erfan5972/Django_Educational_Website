from django.shortcuts import render
from django.views import View
from accounts.models import User
from post.models import Post


class HomeView(View):

    def get(self, request):
        posts = Post.objects.all()
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            return render(request, 'home/home.html', {'user': user, 'posts': posts})
        return render(request, 'home/home.html', {'posts': posts})