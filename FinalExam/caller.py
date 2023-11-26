import os
import django
from django.db.models import Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Author, Review, Article


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    if search_name is not None and search_email is None:
        authors = Author.objects.filter(full_name__icontains=search_name).order_by("-full_name")

    elif search_name is None and search_email is not None:
        authors = Author.objects.filter(email__icontains=search_email).order_by("-full_name")

    else:
        authors = (Author.objects
                   .filter(full_name__icontains=search_name, email__icontains=search_email)
                   .order_by("-full_name"))

    authors_info = [
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned is True else 'Not Banned'}"
        for a in authors
    ]

    return "\n".join(authors_info)


def get_top_publisher():
    top_publisher = Author.objects.get_authors_by_article_count().first()

    if not Article.objects.all():
        return ""

    return f"Top Author: {top_publisher.full_name} with {top_publisher.article_count} published articles."


def get_top_reviewer():
    top_author = (Author.objects.
                  prefetch_related("authors_review").
                  annotate(review_count=Count("authors_review")).
                  order_by("-review_count", "email").first()
                  )

    if not Review.objects.all():
        return ""

    return f"Top Reviewer: {top_author.full_name} with {top_author.review_count} published reviews."


def get_latest_article():
    latest_article = (Article.objects
                      .prefetch_related("articles_review")
                      .annotate(review_count=Count("articles_review"))
                      .order_by("-published_on").first()
                      )

    if not Article.objects.all() or not latest_article:
        return ""

    related_authors_full_name = latest_article.authors.all().order_by("full_name")

    if latest_article.review_count == 0:
        average_rating = 0
    else:
        average_rating = latest_article.articles_review.aggregate(average_rating=Avg("rating"))["average_rating"]

    return (f"The latest article is: {latest_article.title}. "
            f"Authors: {', '.join([a.full_name for a in related_authors_full_name])}. "
            f"Reviewed: {latest_article.review_count} times. "
            f"Average Rating: {average_rating:.2f}.")


def get_top_rated_article():
    top_article = (Article.objects
                   .prefetch_related("articles_review")
                   .annotate(review_rating=Avg("articles_review__rating"))
                   .annotate(review_count=Count("articles_review"))
                   .order_by("-review_rating", "title").first()
                   )

    if not Review.objects.all():
        return ""

    return (f"The top-rated article is: "
            f"{top_article.title}, with an average rating of {top_article.review_rating:.2f}, "
            f"reviewed {top_article.review_count} times.")


def ban_author(email=None):
    if email is None or not Author.objects.all():
        return "No authors banned."

    author = Author.objects.filter(email__iexact=email).annotate(reviews_count=Count("authors_review")).first()

    if not author:
        return "No authors banned."

    author.is_banned = True
    author.save()

    all_author_reviews = author.authors_review.all()

    for r in all_author_reviews:
        r.delete()

    return f"Author: {author.full_name} is banned! {author.reviews_count} reviews deleted."

