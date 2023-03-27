from django.db import models

SUGGESTION_AREA = [
    ('article', 'Article'),
    ('category', 'Category'),
    ('recipe', 'Recipe')
]


class Contact(models.Model):
    """
    A class for the Contact model
    """
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=False)
    email_subscription = models.BooleanField(default=False)
    category = models.CharField(
        choices=SUGGESTION_AREA,
        max_length=100,
        default='Recipe'
        )
    message = models.TextField(blank=False)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name
