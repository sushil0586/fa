from django.contrib import admin

from financial.models import accountHead,account
# Register your models here.


class accountheadAdmin(admin.ModelAdmin):
    list_display = ['name','code','detilsinbs','accountheadsr','entity','owner']
    
class accountAdmin(admin.ModelAdmin):
    list_display = ['accountname','accounthead','accountcode','gstno','entity','owner']


admin.site.register(accountHead, accountheadAdmin)


admin.site.register(account,accountAdmin)
# admin.site.register(account_detials1)
# admin.site.register(account_detials2)
