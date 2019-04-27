from django.db import models
from findance import abstract

from users.models import FindanceUser
from assets.models import AssetOwnership, Asset

class OwningEntity(abstract.BaseFindanceModel):
    """
    An entity that can posses Assets.

    This can be a person, company, anything that can hold onto "stuff"
    """

    # The name of this entity.
    name = models.TextField(unique=True)

    # The Assets that are under this entities domain. This includes
    # partial assets.
    assets = models.ManyToManyField(Asset, through=AssetOwnership)

    def __repr__(self):
        return f"<(OwningEntity, {self.name})>"

    def __str__(self):
        return self.name

class EntityControl(abstract.BaseFindanceModel):
    """
    Permission/Control over a given OwningEntity.
    """

    # The user this control relates to.
    user = models.ForeignKey(FindanceUser, on_delete=models.CASCADE)

    # The owning entity
    entity = models.ForeignKey(OwningEntity, on_delete=models.CASCADE)

    # Ownership type. There are a few different types of permissions
    # when it relates to a given entity
    #
    # Read Owned: The user can see the owned information but none of the partially owned
    #             assets. No editing or management allowed
    #
    # Read All:   The user can see all of the information both owned and partially owned
    #             but has no editing capabilities (default for client)
    #
    # Write:      The user can see all information and manage Assets, Buy, Sell, and other-
    #             wise. No ability to change the entity or it's factors
    #
    # Admin:      The user has complete control over the entity including managing users,
    #             Buy, Sell, or otherwise.
    #
    CONTROL_CHOICES = (
        ( 'o', 'Read Owned' ),
        ( 'r', 'Read All' ),
        ( 'w', 'Write' ),
        ( 'a', 'Admin' ),
    )
    CONTROL_MAP = { k:v for k,v in CONTROL_CHOICES }
    REVERSE_CONTROL_MAP = { v:k for k,v in CONTROL_CHOICES }

    permission = models.CharField(
        max_length=1,
        choices=CONTROL_CHOICES,
        default=REVERSE_CONTROL_MAP['Read All']
    )

    def __repr__(self):
        return f"<(EntityControl, {self.user}, {self.entity})>"

    def __str__(self):
        verbose = CONTROL_MAP[self.permission]
        return f"{self.user} has: {verbose} rights on {self.entity}"
