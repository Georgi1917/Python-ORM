import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions


def create_pet(name: str, species: str) -> str:
    Pet.objects.create(name=name, species=species)

    return f'{name} is a very cute {species}!'


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)

    return f'The artifact {name} is {age} years old!'


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    all_locations = Location.objects.all().order_by('-id')

    location_data = []

    for l in all_locations:
        location_data.append(str(l))

    return '\n'.join(location_data)


def new_capital():
    first_location = Location.objects.first()

    first_location.is_capital = True

    first_location.save()


def get_capitals():
    return Location.objects.all().filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.all().first().delete()


def apply_discount():
    all_cars = Car.objects.all()

    for car in all_cars:
        per_discount = sum([int(x) for x in str(car.year)])

        discount = float(car.price) * (per_discount / 100)

        car.price_with_discount = float(car.price) - discount

        car.save()


def get_recent_cars():
    return Car.objects.all().filter(year__gte=2020).values('model', 'price_with_discount')


def delete_last_car():
    last_car = Car.objects.last()

    last_car.delete()


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.all().filter(is_finished=False)

    list_of_tasks = [str(t) for t in unfinished_tasks]

    return '\n'.join(list_of_tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.pk % 2 == 0:
            continue

        task.is_finished = True

        task.save()


def encode_and_replace(text: str, task_title: str):
    given_tasks = Task.objects.all().filter(title=task_title)
    encoded_text = ''.join([chr(ord(x) - 3) for x in text])

    for task in given_tasks:
        task.description = encoded_text

        task.save()


def get_deluxe_rooms():
    all_deluxe_rooms = HotelRoom.objects.all().filter(room_type='Deluxe')

    all_room_str = [str(x) for x in all_deluxe_rooms if x.pk % 2 == 0]

    return '\n'.join(all_room_str)


def increase_room_capacity():
    all_reserved_rooms = HotelRoom.objects.all().filter(is_reserved=True).order_by('id')

    previous_room_capacity = None

    for room in all_reserved_rooms:
        if previous_room_capacity is None:
            room.capacity += room.pk
            previous_room_capacity = room.capacity

        else:
            room.capacity += previous_room_capacity
            previous_room_capacity = room.capacity

        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()

    first_room.is_reserved = True

    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if last_room.is_reserved is True:
        last_room.delete()


def update_characters():
    all_characters = Character.objects.all()

    for char in all_characters:
        if char.class_name == 'Mage':
            char.level += 3
            char.intelligence -= 7
        elif char.class_name == 'Warrior':
            char.hit_points = char.hit_points // 2
            char.dexterity += 4
        else:
            char.inventory = 'The inventory is empty'

        char.save()


def fuse_characters(first_character: Character, second_character: Character):
    new_name = f'{first_character.name} {second_character.name}'
    new_class_name = 'Fusion'
    new_level = (first_character.level + second_character.level) // 2
    new_strength = (first_character.strength + second_character.strength) * 1.2
    new_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    new_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    new_hit_points = (first_character.hit_points + second_character.hit_points)

    if first_character.class_name in ('Mage', 'Scout'):
        new_inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    else:
        new_inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=new_name,
        class_name=new_class_name,
        level=int(new_level),
        strength=int(new_strength),
        dexterity=int(new_dexterity),
        intelligence=int(new_intelligence),
        hit_points=new_hit_points,
        inventory=new_inventory
    )

    Character.objects.filter(id=first_character.pk).delete()
    Character.objects.filter(id=second_character.pk).delete()


def grand_dexterity():
    all_rows = Character.objects.all()

    for char in all_rows:
        char.dexterity = 30
        char.save()


def grand_intelligence():
    all_rows = Character.objects.all()

    for char in all_rows:
        char.intelligence = 40
        char.save()


def grand_strength():
    all_rows = Character.objects.all()

    for char in all_rows:
        char.strength = 50
        char.save()


def delete_characters():
    Character.objects.all().filter(inventory='The inventory is empty').delete()


update_characters()