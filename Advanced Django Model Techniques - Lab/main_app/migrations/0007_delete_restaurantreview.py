# Generated by Django 4.2.4 on 2023-11-08 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_menureview_delete_restaurantreview_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RestaurantReview',
        ),
    ]
