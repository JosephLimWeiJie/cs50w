# Generated by Django 3.0.8 on 2020-09-22 12:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('order_total_price', models.FloatField(blank=True, null=True)),
                ('has_new_notification', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('desrc', models.TextField()),
                ('category', models.CharField(blank=True, choices=[("Men's Wear", "Men's Wear"), ("Women's Apparel", "Women's Apparel"), ('Mobile & Gadgets', 'Mobile & Gadgets'), ('Beauty & Personal Care', 'Beauty & Personal Care'), ('Home Appliances', 'Home Appliances'), ('Home & Living', 'Home & Living'), ('Kids Fashion', 'Kids Fashion'), ('Toys, Kids & Babies', 'Toys, Kids & Babies'), ('Video Games', 'Video Games'), ('Food & Beverages', 'Food & Beverages'), ('Computers & Peripherals', 'Computers & Peripherals'), ('Hobbies & Books', 'Hobbies & Books'), ('Health & Wellness', 'Health & Wellness'), ("Women's Bags", "Women's Bags"), ('Travel & Luggage', 'Travel & Luggage'), ('Pet Food & Supplies', 'Pet Food & Supplies'), ('Watches', 'Watches'), ('Jewellery & Accessory', 'Jewellery & Accessory'), ("Men's Shoes", "Men's Shoes"), ("Women's Shoes", "Women's Shoes"), ('Sports & Outdoors', 'Sports & Outdoors'), ('Automotive', 'Automotive'), ("Men's Bags", "Men's Bags"), ('Cameras & Drones', 'Cameras & Drones'), ('Dining, Travel & Services', 'Dining, Travel & Services'), ('Miscellaneous', 'Miscellaneous')], max_length=64)),
                ('datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('listing_main_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('rating_score', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('quantity_sold', models.IntegerField(default=0)),
                ('click_rate', models.IntegerField(default=0)),
                ('is_sold_out', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=100)),
                ('gender', models.CharField(default='Male', max_length=20)),
                ('phone_number', models.IntegerField(blank=True, default=99887766)),
                ('date_of_birth', models.DateField(default='2000-12-30')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('delivery_address', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('listing', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='review', to='shopping.Listing')),
                ('profile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='review', to='shopping.Profile')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_demanded', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('To Ship', 'To Ship'), ('To Receive', 'To Receive'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Return/Refund', 'Return/Refund'), ('Return Rejected', 'Return Rejected')], default='To Ship', max_length=64)),
                ('has_purchased', models.BooleanField(default=False)),
                ('is_tracking', models.BooleanField(default=False)),
                ('listing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='shopping.Listing')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('has_read', models.BooleanField(default=False)),
                ('has_action', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('listing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='shopping.Listing')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='shopping.Order')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='shopping.Profile')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='shopping.Review')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('listing', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shopping.Listing')),
            ],
        ),
    ]
