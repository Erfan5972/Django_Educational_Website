from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Post, PostVideo

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Post)
admin.site.register(PostVideo)