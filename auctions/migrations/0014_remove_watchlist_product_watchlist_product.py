# Generated by Django 5.0 on 2023-12-19 22:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_watchlist_product_watchlist_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='product',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
