# Generated by Django 3.2.16 on 2022-12-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.TextField()),
                ('email_subscription', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('Article', 'article'), ('Category', 'category'), ('Recipe', 'recipe')], default='Recipe', max_length=100)),
                ('message', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]
