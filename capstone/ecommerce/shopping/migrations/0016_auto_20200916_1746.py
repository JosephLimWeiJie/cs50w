# Generated by Django 3.0.8 on 2020-09-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0015_notification_has_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('To Ship', 'To Ship'), ('To Receive', 'To Receive'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Return/Refund', 'Return/Refund'), ('Return Rejected', 'Return Rejected')], default='To Ship', max_length=64),
        ),
    ]
