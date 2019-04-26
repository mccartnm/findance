from django.db import models
from findance import abstract

class Asset(abstract.BaseFindanceModel):
    """
    An ownable item.
    """ 

    # The unique name of the item. Many of these can be owned
    # through a form of ownership
    name = models.TextField(unique=True)

    # The description of an Asset. Need a way to "wiki" this
    # so it can be handled more easily.
    description = models.TextField(default="", blank=True, null=True)

    # The root value of an item (based again USD) at all times.
    # This way converting can always be done against USD
    value = abstract.MonetaryField()

    def __repr__(self):
        return f"<(Asset, {self.name})>"

    def __str__(self):
        return self._name


class AssetOwnership(abstract.BaseFindanceModel):
    """
    ManyToMany through table that represents part or total ownership
    over an Asset.
    """

    # The asset that our enitity has some control over, be it to look
    # sell, etc.
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    # The owner of this item
    owner = models.ForeignKey('entity.OwningEntity', on_delete=models.CASCADE)

    # The amount of ownership this entity has on an asset. Anything
    # >= 100% is considers to be total ownership.
    # This is kept is a 0.0 - 1.0 value for the same of simple
    # arithmatic
    percentage = abstract.MonetaryField()

    # The number of this Asset owned by the owner. This saves us from
    # duplicate rows in the database which would cause unwanted stress
    # on the table size.
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = (('asset', 'owner'),)

    def __repr__(self, *args, **kwargs):
        return f"<(AssetOwnership, {self.owner}, {self.asset}, {self.count})>"

    def __str__(self):
        return f"{self.owner} - {self.asset} ({self.count})"