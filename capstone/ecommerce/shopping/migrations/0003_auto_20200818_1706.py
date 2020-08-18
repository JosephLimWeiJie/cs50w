# Generated by Django 3.0.8 on 2020-08-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_auto_20200818_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default='0'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='hi@example.com', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default='Male', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(blank=True, default=99887766),
        ),
    ]
