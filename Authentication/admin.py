from django.contrib import admin
from Authentication.models import User,Role,MainMenu,submenu,rolepriv

admin.site.register(User)

admin.site.register(Role)
admin.site.register(MainMenu)
admin.site.register(submenu)
admin.site.register(rolepriv)

# Register your models here.
