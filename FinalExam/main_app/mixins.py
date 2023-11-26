from django.core.validators import MinLengthValidator
from django.db import models


class PublishedOnMixIn(models.Model):
    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        abstract = True


class ContentMixIn(models.Model):
    content = models.TextField(
        validators=[MinLengthValidator(10)]
    )

    class Meta:
        abstract = True