# Generated by Django 3.2.16 on 2022-11-16 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_category_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='instruction',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='author',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='likes',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
        migrations.DeleteModel(
            name='Instruction',
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
    ]
