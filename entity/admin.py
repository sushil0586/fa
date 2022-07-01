from io import UnsupportedOperation
from django.contrib import admin
from entity.models import unitType,entity,entity_details


# Register your models here.



class unitTypeAdmin(admin.ModelAdmin):
    list_display = ['UnitName','UnitDesc','createdby']

class entityeAdmin(admin.ModelAdmin):
    list_display = ['unitType','entityName','address']

admin.site.register(unitType,unitTypeAdmin)

admin.site.register(entity,entityeAdmin)
admin.site.register(entity_details)

