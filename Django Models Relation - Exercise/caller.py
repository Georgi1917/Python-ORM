import datetime
import os
from datetime import date

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Registration, Car, \
    Owner


def show_all_authors_with_their_books():
    authors_with_books = []
    authors = Author.objects.all().order_by("id")

    for author in authors:
        books = Book.objects.filter(author=author)

        if not books:
            continue

        title = ', '.join(x.title for x in books)
        authors_with_books.append(f"{author.name} has written - {title}!")

    return "\n".join(authors_with_books)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    song.artists.add(artist)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.all().order_by("-id")
    return songs


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = Review.objects.filter(product=product)

    total_sum = sum(review.rating for review in reviews)
    count_of_reviews = reviews.count()

    return total_sum / count_of_reviews


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by("-name")


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    return "\n".join(str(x) for x in DrivingLicense.objects.all().order_by("-license_number"))


def get_drivers_with_expired_licenses(due_date):
    drivers = Driver.objects.all()
    drivers_with_expired_license = []

    for driver in drivers:
        driver_exp_date = driver.drivinglicense.issue_date + datetime.timedelta(days=365)

        if driver_exp_date > due_date:
            drivers_with_expired_license.append(driver)

    return drivers_with_expired_license


def register_car_by_owner(owner: object):
    first_registration = Registration.objects.filter(car__isnull=True).first()
    first_car = Car.objects.filter(registration__isnull=True, owner=owner).first()

    first_registration.car = first_car
    first_registration.registration_date = date.today()
    first_car.owner = owner

    first_registration.save()
    first_car.save()

    return (f"Successfully registered {first_car.model} to {owner.name} with "
            f"registration number {first_registration.registration_number}.")



