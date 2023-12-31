# Generated by Django 4.2.4 on 2023-10-25 12:36

from django.db import migrations


def change_age_group(apps, schema_editor):
    person_model = apps.get_model('main_app', 'Person')

    all_persons = person_model.objects.all()

    for person in all_persons:
        if person.age <= 12:
            person.age_group = 'Child'
        elif person.age <= 17:
            person.age_group = 'Teen'
        else:
            person.age_group = 'Adult'
        person.save()


def reverse_age_group(apps, schema_editor):
    person_model = apps.get_model('main_app', 'Person')

    all_persons = person_model.objects.all()

    for person in all_persons:
        person.age_group = 'no age group'

        person.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_person'),
    ]

    operations = [
        migrations.RunPython(change_age_group, reverse_age_group)
    ]
