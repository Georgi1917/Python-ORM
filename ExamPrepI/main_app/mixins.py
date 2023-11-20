from django.db import models


class LastUpdatedMixIn(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(
        auto_now=True
    )


class IsAwardedMixIn(models.Model):
    is_awarded = models.BooleanField(
        default=False
    )

    class Meta:
        abstract = True