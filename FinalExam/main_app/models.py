from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import AuthorManager
from main_app.mixins import PublishedOnMixIn, ContentMixIn


# Create your models here.


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )
    email = models.EmailField(
        unique=True
    )
    is_banned = models.BooleanField(
        default=False
    )
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005)
        ]
    )
    website = models.URLField(
        null=True,
        blank=True
    )

    objects = AuthorManager()


class Article(PublishedOnMixIn, ContentMixIn):
    cat_choices = [
        ("Technology", "Technology"),
        ("Science", "Science"),
        ("Education", "Education"),
    ]

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5)
        ]
    )
    category = models.CharField(
        max_length=10,
        choices=cat_choices,
        default="Technology"
    )
    authors = models.ManyToManyField(
        to=Author,
        related_name="authors_article"
    )


class Review(PublishedOnMixIn, ContentMixIn):
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name="authors_review"
    )
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name="articles_review"
    )