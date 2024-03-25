from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to='post/image/')
    description = models.TextField()
    is_premium = models.BooleanField(default=False)
    price = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['title', 'is_premium']

    def __str__(self):
        return f'{self.title} - {self.is_premium} - {self.price}'


class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postvideos')
    video = models.FileField()


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='category/image/')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'name: {self.name} - parent:  {self.parent}'