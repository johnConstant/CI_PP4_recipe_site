from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from category.models import Category


STATUS = ((0, 'Draft'), (1, 'Published'))
DIFFICULTY_LEVEL = [
    ('Beginner', 'beginner'),
    ('Medium', 'medium'),
    ('Advanced', 'advanced')
]


class Recipe(models.Model):
    """
    A class view creating the Recipe model
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    featured_image = CloudinaryField('image', default='placeholder')
    categories = models.ManyToManyField(
        Category, related_name='recipe_categories', blank=True
        )
    featured_recipe = models.BooleanField(default=False)
    cook_time = models.IntegerField()
    prep_time = models.IntegerField()
    servings = models.IntegerField()
    difficulty = models.CharField(
        choices=DIFFICULTY_LEVEL,
        max_length=100,
        default='Beginner'
        )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='recipe_author'
        )
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='recipe_likes', blank=True
        )
    created_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def total_time(self):
        return self.prep_time + self.cook_time


class Comment(models.Model):
    """
    A class view creating the Comment model
    """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments'
        )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=0)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class Instruction(models.Model):
    """
    A class view creating the Instruction model
    """
    body = models.TextField(blank=False)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_instruction'
        )

    def __str__(self):
        return self.body


class Ingredient(models.Model):
    """
    A class view creating the Ingredient model
    """
    amount = models.CharField(max_length=100, unique=False)
    name = models.CharField(max_length=200, unique=False)
    notes = models.TextField(blank=True)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient'
        )

    def __str__(self):
        return self.name
