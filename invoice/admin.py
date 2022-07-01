from django.contrib import admin
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails,journal,salereturn,salereturnDetails,Transactions



class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['account','transactiontype','desc','drcr','amount','entity','createdby']


# Register your models here.

admin.site.register(SalesOderHeader)
admin.site.register(salesOrderdetails)

admin.site.register(purchaseorder)
admin.site.register(PurchaseOrderDetails)
admin.site.register(salereturn)
admin.site.register(salereturnDetails)
admin.site.register(journal)
admin.site.register(Transactions,TransactionsAdmin)