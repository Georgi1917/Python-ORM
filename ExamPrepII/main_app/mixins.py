from django.db import models


class CreationDateMixIn(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(
        auto_now_add=True
    )