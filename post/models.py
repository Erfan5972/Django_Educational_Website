from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from moviepy.editor import VideoFileClip
from django.urls import reverse
from accounts.models import User


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

    def get_absolute_url(self):
        return reverse('post:detail', args=[self.id])


class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postvideos')
    video = models.FileField()
    duration = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.video:
            try:
                clip = VideoFileClip(self.video.path)
                duration_in_seconds = clip.duration
                duration_in_minutes = int(duration_in_seconds // 60)
                duration_in_seconds_remainder = int(duration_in_seconds % 60)
                self.duration = f"{duration_in_minutes}:{duration_in_seconds_remainder}"
            except Exception as e:
                print(f"Error occurred while getting video duration: {e}")
        super().save(*args, **kwargs)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='category/image/')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'name: {self.name} - parent:  {self.parent}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='p_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' user: {self.user} -post: {self.post}'