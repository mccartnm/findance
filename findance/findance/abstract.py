"""
Abstract models that we use throughout 
"""
import uuid
import itertools
import functools
from datetime import datetime, timezone, timedelta
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db import models

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets

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


class BaseFindanceAPI(viewsets.ModelViewSet):
    """
    Root ViewSet that we use for most models. This is similar to a ModelViewSet
    except we have control over an additional search parameter if we're not using
    the pk (id) to lookup our model. This makes it easier to query for something
    in a human readable format (e.g. username "jdoe" rather than user id '1451532321451')
    """
    serializer = None       # Where we get the model from
    search_alternate = None # If we don't provide an id, another field we may use
    order_by_field = 'id'   # By default, we use the id of the model (which is created date)

    # -- Virtual function from ModelViewSet
    def get_serializer_class(self):
        return self.serializer

    def get_queryset(self):
        """
        Custom queryset can be used for the pagination toolkit
        """
        if getattr(self, 'use_this_queryset', None):
            return self.use_this_queryset
        return self.model().objects.all()

    # -- Virtual Interafce
    def list_class_search(self, request, current_queryset):
        """
        When using the list() command (GET singular or batch), this
        is called to add any additional logic to the queryset or verify
        the user has access to the items being pulled.

        :param request: The django request object that comes without view
        :param current_queryset: The QuerySet that we're actively working on
        :return: QuerySet that we'll be using to fetch the objects.
        """
        return current_queryset

    @classmethod
    def model(cls):
        return cls.serializer.Meta.model

    @classmethod
    def _get_object(cls, pk):
        """
        Based on the alloted keys, attempt to find an object by either
        it's id or the item in question
        """
        kwargs = {}
        try:
            kwargs['pk'] = int(pk)
        except Exception as e:
            if not cls.search_alternate:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            kwargs[f"{cls.search_alternate}__iexact"] = pk
        return get_object_or_404(cls.model().objects.all(), **kwargs)

    def get_permissions(self):
        """
        Default permissions on this endpoint.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, format=None):
        """
        Generalized GET request on model.
        """
        get_data = request.GET
        page = None

        search_params = {}
        exlude_params = {}
        for k, v in request.GET.items():
            if k.startswith('search_'):
                search_params[k[len('search_'):]] = v
            elif k.startswith('exclude_'):
                exlude_params[k[len('exclude_'):]] = v

        if self.search_alternate and self.search_alternate in get_data:
            objects = self.model().objects.filter(
                **{f'{self.search_alternate}__iexact': get_data[self.search_alternate]}
            )
            if not objects.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif search_params or exlude_params:
            objects = self.model().objects.filter(
                **search_params
            ).exclude(
                **exlude_params
            ).order_by(self.order_by_field)
        else:
            objects = self.model().objects.all().order_by(self.order_by_field)

        objects = self.list_class_search(request, objects)

        page = self.paginate_queryset(objects)
        if page is not None:
            serializer = self.serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer(
            objects, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None, format=None):
        """
        Lookup a single currency by it's code rather than id
        """
        currency = self._get_object(pk)
        serializer = self.serializer(currency, context={'request': request})
        return Response(serializer.data)

    def create(self, request, format=None):
        """
        Create an object
        """
        serializer = self.serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            new_currency = self.model().objects.create(**serializer.validated_data)
            return Response(
                self.serializer(
                    new_currency, context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, format=None):
        """
        Update a given currency by code or id
        """
        currency = self._get_object(pk)
        serializer = self.serializer(currency, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(self.serializer(currency, context={'request': request}).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
