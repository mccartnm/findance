from findance.abstract import BaseFindanceModel, MonetaryField
from simple_history.models import HistoricalRecords
from django.db import models

class Currency(BaseFindanceModel):
    """
    Control over a currency begins with the currency itself!
    """

    # ISO code that this currency is known for. Should never be
    # longer than 3 characters but postgres treats Char and Text
    # the same so who cares!
    code = models.TextField(unique=True)

    # The fullname of the currency for display purposes
    fullname = models.TextField()

    # The last recorded rate for this model. 
    rate = MonetaryField()

    # Keep tabs as this currency changes
    history = HistoricalRecords()

    def __repr__(self):
        return f"<(Currency {self.code} {self.rate})>"

    def __str__(self):
        return f"{self.code} - {self.fullname}"
