from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, 'Draft'), (1, 'Published'))
DIFFICULTY_LEVEL = [
    (0, 'Beginner'),
    (1, 'Medium'),
    (2, "Advanced")
]


class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    featured_image = CloudinaryField('image', default='placeholder')
    categories = models.ManyToManyField(User, related_name='recipe_categories', blank=True)
    featured_recipe = models.BooleanField(default=False)
    cook_time = models.IntegerField()
    prep_time = models.IntegerField()
    servings = models.IntegerField()
    difficulty = model.IntegerField(choices=DIFFICULTY_LEVEL, default=1)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipe_author'
        )  
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='recipe_likes', blank=True)
    created_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()