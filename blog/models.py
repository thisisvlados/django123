from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250) #текстовое поле
    slug = models.SlugField(max_length=250, unique_for_date='publish') #способ для генерации URL
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE) #сообщаем о том, что каждая запись написана пользователем, и пользователь можетсоздать сколько угодно постов
    body = models.TextField() #тело поста
    publish = models.DateTimeField(default=timezone.now) #дата публикации поста
    created = models.DateTimeField(auto_now_add=True) #дата создания поста
    updated = models.DateTimeField(auto_now=True) #когда изменили пост
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',) #чтобы последний пост был на первом месте

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"Comment by {self.email} on {self.name} on {self.post}"
