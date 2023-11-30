from django.db import models

from enums import CreatedModelEnum


class CreatedModel(models.Model):
    """
    Abstract model that adds a creation date.

    Attributes:
        pub_date (models.DateTimeField): The date and time when the model instance was created.
    """

    pub_date: models.DateTimeField = models.DateTimeField(
        CreatedModelEnum.PUB_DATE_VERBOSE_NAME.value,
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract: bool = True
