from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, 'Draft'), (1, 'Published'))
TOPICS = (
    ('tips', 'Tips & Tricks'),
    ('review', 'Reviews'),
    ('technique', 'Techniques'),
    ('article', 'Article')
    )


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='article'
        )
    topic = models.CharField(
        choices=TOPICS,
        max_length=100,
        default='Article'
        )
    created_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='article_likes', blank=True
        )

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments'
        )
    name = models.CharField(max_length=80, unique=True)
    email = models.EmailField()
    body = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=0)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
