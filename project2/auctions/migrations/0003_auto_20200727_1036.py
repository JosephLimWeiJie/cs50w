# Generated by Django 3.0.8 on 2020-07-27 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='bid',
            new_name='current_bid',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
    ]
