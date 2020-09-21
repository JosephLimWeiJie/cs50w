# Generated by Django 3.0.8 on 2020-09-21 14:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0022_listing_is_sold_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='rating_score',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
