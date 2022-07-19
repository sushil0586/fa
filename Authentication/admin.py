from django.contrib import admin
from Authentication.models import User,Role,MainMenu,submenu

admin.site.register(User)

admin.site.register(Role)
admin.site.register(MainMenu)
admin.site.register(submenu)

# Register your models here.
