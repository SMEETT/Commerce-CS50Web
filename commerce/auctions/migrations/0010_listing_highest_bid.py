# Generated by Django 3.0.8 on 2020-07-29 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200727_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='highest_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
