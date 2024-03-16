from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'base.html')

    def post(self, request):
        pass