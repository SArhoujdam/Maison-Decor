# Generated by Django 5.2 on 2025-06-13 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Categories', '0005_produit_slug'),
        ('PFE', '0009_commande_created_at_commande_produits_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('prix_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PFE.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Categories.produit')),
            ],
        ),
    ]
