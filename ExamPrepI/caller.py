import os
import django
from django.db.models import Count, Avg, F

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


def get_actors_by_movies_count():
    actors = (Actor.objects.
              prefetch_related("actors_movies").
              annotate(movies_count=Count("actors_movies")).
              filter(movies_count__gt=0).order_by("-movies_count", "full_name"))[:3]

    if not actors or not Movie.objects.all():
        return ""

    actor_info = [
        f"{a.full_name}, participated in {a.movies_count} movies"
        for a in actors
    ]

    return "\n".join(actor_info)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(is_awarded=True).order_by("-rating", "title").first()

    if not top_movie:
        return ""

    return (f"Top rated awarded movie: {top_movie.title}, "
            f"rating: {top_movie.rating:.1f}. "
            f"Starring actor: {'N/A' if not top_movie.starring_actor else top_movie.starring_actor.full_name}. "
            f"Cast: {', '.join(a.full_name for a in top_movie.actors.all())}.")


def increase_rating():
    value_to_increase = 0.1

    classic_movies = (Movie.objects.
                      filter(is_classic=True, rating__lt=10)
                      .update(rating=F("rating") + value_to_increase))

    if not classic_movies:
        return "No ratings increased."

    return f"Rating increased for {classic_movies} movies."



