# Generated by Django 4.2.4 on 2023-10-25 16:29

from django.db import migrations


def set_rarity(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')

    all_items = item_model.objects.all()

    for item in all_items:
        if item.price <= 10:
            item.rarity = 'Rare'
        elif 11 <= item.price <= 20:
            item.rarity = 'Very Rare'
        elif 21 <= item.price <= 30:
            item.rarity = 'Extremely Rare'
        else:
            item.rarity = 'Mega Rare'
        item.save()


def reverse_rarity(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')

    all_items = item_model.objects.all()

    for item in all_items:
        item.rarity = 'no rarity'
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_rarity, reverse_rarity)
    ]