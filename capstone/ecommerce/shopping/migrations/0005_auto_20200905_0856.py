# Generated by Django 3.0.8 on 2020-09-05 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_auto_20200905_0614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='listing',
        ),
        migrations.AddField(
            model_name='listing',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='shopping.Order'),
        ),
    ]
