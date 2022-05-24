from django.contrib import admin

from financial.models import accountHead,account,account_detials1,account_detials2
# Register your models here.

admin.site.register(accountHead)
admin.site.register(account)
admin.site.register(account_detials1)
admin.site.register(account_detials2)
