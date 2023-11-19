from decimal import Decimal

from django.db import models
from django.db.models import Count, Max, Min, Avg


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(price__range=[min_price, max_price])

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self):
        return self.annotate(location_count=Count("location")).order_by("-location_count", "id").values("id", "location")[:2]


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        highest_rated = self.aggregate(highest_rating=Max("rating"))["highest_rating"]
        return self.get(rating=highest_rated)

    def lowest_rated_game(self):
        lowest_rated = self.aggregate(lowest_rating=Min("rating"))["lowest_rating"]
        return self.get(rating=lowest_rated)

    def average_rating(self):
        return f"{self.aggregate(avg_rating=Avg('rating'))['avg_rating']:.1f}"