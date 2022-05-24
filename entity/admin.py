from io import UnsupportedOperation
from django.contrib import admin
from entity.models import unitType,entity,entity_details

# Register your models here.

admin.site.register(unitType)

admin.site.register(entity)
admin.site.register(entity_details)

