
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import AbstractUser
from findance.abstract import BaseFindanceModel
from django.db import models

class FindanceUser(AbstractUser, BaseFindanceModel):
    """
    The Findance user model,
    """

    # The entities this user has some level of visibility/control over.
    # If the permission does not exist, we assume the user has no
    # access.
    entities = models.ManyToManyField('entity.OwningEntity', through='entity.EntityControl')

    # The history of our users is important. While they should rarely
    # change it's better to be sure.
    history = HistoricalRecords()
