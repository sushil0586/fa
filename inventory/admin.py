from django.contrib import admin
from inventory.models import Album,Track,Product,ProductCategory


admin.site.register(Album)
admin.site.register(Track)
admin.site.register(ProductCategory)
admin.site.register(Product)


# Register your models here.
