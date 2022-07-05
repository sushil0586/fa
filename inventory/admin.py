from django.contrib import admin
from inventory.models import Album,Track,Product,ProductCategory,UnitofMeasurement,typeofgoods,stkvaluationby,stkcalculateby,Ratecalculate,gsttype


admin.site.register(Album)
admin.site.register(Track)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(UnitofMeasurement)
admin.site.register(typeofgoods)
admin.site.register(stkvaluationby)
admin.site.register(stkcalculateby)
admin.site.register(Ratecalculate)
admin.site.register(gsttype)


# Register your models here.
