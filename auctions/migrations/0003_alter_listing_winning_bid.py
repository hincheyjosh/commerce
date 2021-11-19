# Generated by Django 3.2.7 on 2021-10-01 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_winning_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='winning_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='auctions.bid'),
        ),
    ]
