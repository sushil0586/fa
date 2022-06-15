from django.contrib import admin

from financial.models import accountHead,account
# Register your models here.

class AccountheadAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(accountHead, AccountheadAdmin)


admin.site.register(account)
# admin.site.register(account_detials1)
# admin.site.register(account_detials2)
