from django.contrib import admin
from geography.models import country,state,district,city

# Register your models here.

admin.site.register(country)

admin.site.register(state)

admin.site.register(district)

admin.site.register(city)
