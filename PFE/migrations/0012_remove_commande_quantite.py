# Generated by Django 5.2 on 2025-06-15 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFE', '0011_remove_commande_produits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='quantite',
        ),
    ]
