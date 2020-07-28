# Generated by Django 3.0.8 on 2020-07-28 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_is_on_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[("Men's Wear", "Men's Wear"), ("Women's Apparel", "Women's Apparel"), ('Mobile & Gadgets', 'MMobile & Gadgets'), ('Beauty & Personal Care', 'Beauty & Personal Care'), ('Home Appliances', 'Home Appliances'), ('Home & Living', 'Home & Living'), ('Kids Fashion', 'Kids Fashion'), ('Toys, Kids & Babies', 'Toys, Kids & Babies'), ('Video Games', 'Video Games'), ('Food & Beverages', 'Food & Beverages'), ('Computers & Peripherals', 'Computers & Peripherals'), ('Hobbies & Books', 'Hobbies & Books'), ('Health & Wellness', 'Health & Wellness'), ("Women's Bags", "Women's Bags"), ('Travel & Luggage', 'Travel & Luggage'), ('Pet Food & Supplies', 'Pet Food & Supplies'), ('Watches', 'Watches'), ('Jewellery & Accessory', 'Jewellery & Accessory'), ("Men's Shoes", "Men's Shoes"), ("Women's Shoes", "Women's Shoes"), ('Sports & Outdoors', 'Sports & Outdoors'), ('Automotive', 'Automotive'), ("Men's Bags", "Men's Bags"), ('Cameras & Drones', 'Cameras & Drones'), ('Dining, Travel & Services', 'Dining, Travel & Services'), ('Miscellaneous', 'Miscellaneous')], max_length=64),
        ),
    ]
