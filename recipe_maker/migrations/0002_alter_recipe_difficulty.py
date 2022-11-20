# Generated by Django 3.2.16 on 2022-11-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_maker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Medium', 'Medium'), ('Advanced', 'Advanced')], default='Beginner', max_length=100),
        ),
    ]