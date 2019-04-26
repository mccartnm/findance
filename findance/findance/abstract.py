"""
Abstract models that we use throughout 
"""
import uuid
import itertools
from datetime import datetime, timezone, timedelta
from django.db import connection
from django.db import models

FINDANCE_EPOCH = datetime(2015, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
BASIC_TICK = itertools.count()
SHARD_ID = 1

class FindanceIdField(models.BigIntegerField):
    """ Base field for primary keys within Findance """

    @staticmethod
    def date_to_int(datetime):
        """
        :param datetime: Timezone aware datetime that we're converting to an int
        :return: int
        """
        diff = datetime - FINDANCE_EPOCH
        delta = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)
        return int(delta)

    @staticmethod
    def _build_id():
        """
        Python menthod of constructing an id a-la instagrams setup
        https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c

        Will eventually want to move this to postgress like they did
        """
        # 1: Timestamp
        current_id = FindanceIdField.date_to_int(datetime.utcnow().replace(tzinfo=timezone.utc)) << 23

        # 2: Shard ID (For now, always one)
        current_id |= SHARD_ID << 10

        # 3: Auto-incr with the last 10 bits
        current_id |= next(BASIC_TICK) % 1024

        return current_id

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', FindanceIdField._build_id)
        super().__init__(*args, **kwargs)


class MonetaryField(models.DecimalField):
    """
    Basic monetary field. Used for most curreny-related fields
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 1.0)
        kwargs['max_digits'] = kwargs.get('max_digits', 64)          # We like big numbers here
        kwargs['decimal_places'] = kwargs.get('decnimal_places', 10) # Some fine precision!
        super().__init__(*args, **kwargs)


class FindanceManager(models.Manager):
    """ Manager that has the ability to search by date on findance items """

    SEARCH_TYPES = ("before", "after", "between")

    def _where_sql_before(self):
        return f"(\"{self.model.db_table}\".id < %s)"

    def _where_sql_after(self):
        return f"(\"{self.model.db_table}\".id > %s)"

    def _where_sql_between(self):
        return f"(\"{self.model.db_table}\".id >= %s AND \"{self.model.db_table}\".id <= %s)"

    def created_search(self, date_a: datetime, date_b: datetime=None, search_type: str=None):
        """
        Custom search based on the search type required.
        :param date_a: datetime()
        :param date_b: datetime() (required when search_type==between)
        :param search_type: str one of (before, after, between)
        :return RawQuerySet:
        """
        where = "" 
        params = [FindanceIdField.date_to_int(date_a)]
        if search_type == "before":
            where = self._where_sql_before()
        elif search_type == "after":
            where = self._where_sql_after()
        elif search_type == "between":
            if not date_b:
                raise ValueError("Between queries require a secondary date!")
            where = self._where_sql_between()
            params.append(FindanceIdField.date_to_int(date_b))

        return self.raw(
            f"SELECT * FROM {self.model.db_table} WHERE {where}",
            params
        )

    def created_before(self, date: datetime):
        """
        Quick function for created_search for before the given date
        """
        return self.created_search(date, search_type="before")

    def created_after(self, date: datetime):
        """
        Quick function for created_search for after a given date
        """
        return self.created_search(date, search_type="after")

    def created_between(self, date_a: datetime, date_b: datetime):
        """
        Quick function to check if the created date is between two
        dates
        """
        return self.created_search(date_a, date_b, search_type="between")


class BaseFindanceModel(models.Model):
    """ Root abstract model for all models used by findance """

    # The primary key that also holds our creation datetime
    id = FindanceIdField(primary_key=True)

    # Custom manager to provide searching on creation timestamps
    # embeded within the primary key
    objects = FindanceManager()

    class Meta:
        """ This is an abstract model """
        abstract = True
        ordering = ('id',)

    @property
    def created(self):
        """
        :return: datetime() that this object was created on
        """
        return FINDANCE_EPOCH + timedelta(microseconds=(self.id >> 23) * 1000)
