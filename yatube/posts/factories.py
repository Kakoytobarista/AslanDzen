import factory
from faker import Faker

from . import models

fake = Faker()


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    text = factory.Sequence(lambda n: f"{fake.text()}")
