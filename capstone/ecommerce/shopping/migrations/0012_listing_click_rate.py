# Generated by Django 3.0.8 on 2020-09-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0011_order_has_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='click_rate',
            field=models.IntegerField(default=0),
        ),
    ]
