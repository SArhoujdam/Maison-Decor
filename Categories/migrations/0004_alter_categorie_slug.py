# Generated by Django 5.2 on 2025-04-13 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Categories', '0003_categorie_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
