import os
import django
from django.db.models import Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    directors = None

    if search_name is None and search_nationality is None:
        return ""

    if search_name is None and search_nationality is not None:
        directors = Director.objects.filter(nationality__icontains=search_nationality).order_by("full_name")

    if search_name is not None and search_nationality is None:
        directors = Director.objects.filter(full_name__icontains=search_name).order_by("full_name")

    if search_name is not None and search_nationality is not None:
        directors = Director.objects.filter(
            full_name__icontains=search_name,
            nationality__icontains=search_nationality).order_by("full_name")

    dir_info = [
        f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}"
        for d in directors
    ]

    return "\n".join(dir_info)


def get_top_director():
    top_dir = Director.objects.get_directors_by_movies_count().first()

    if not top_dir:
        return ""

    return f"Top Director: {top_dir.full_name}, movies: {top_dir.movies_count}."


def get_top_actor():
    top_actor = (Actor.objects.annotate(
        movies_count=Count("starring_movies"))
              .order_by("-movies_count", "full_name")
              .first()
              )

    if top_actor is None or not top_actor.starring_movies.all().exists():
        return ""

    avg_rating = top_actor.starring_movies.aggregate(
        average_rating=Avg("rating"))["average_rating"]

    return (f"Top Actor: {top_actor.full_name}, starring in movies: "
            f"{', '.join([m.title for m in top_actor.starring_movies.all()])}, "
            f"movies average rating: {avg_rating:.1f}")


