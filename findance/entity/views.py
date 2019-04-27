
from findance import abstract
from .models import OwningEntity, EntityControl
from .serializers import OwningEntitySerializer, EntityControlSerializer

class OwningEntityAPI(abstract.BaseFindanceAPI):
    serializer = OwningEntitySerializer
    search_alternate = 'name'

class EntityControlAPI(abstract.BaseFindanceAPI):
    serializer = EntityControlSerializer
    search_alternate = None # For the moment
