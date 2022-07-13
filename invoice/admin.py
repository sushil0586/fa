from django.contrib import admin
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails,journal,salereturn,salereturnDetails,Transactions,StockTransactions,Purchasereturndetails,PurchaseReturn,journalmain,journaldetails

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['account','transactiontype','desc','drcr','amount','entity','createdby']

class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['accounthead','account','transactiontype','desc','debitamount','creditamount']


class journalAdmin(admin.ModelAdmin):
    list_display = ['voucherno','vouchertype','account','drcr','amount','entrydate']

# Register your models here.

admin.site.register(SalesOderHeader)
admin.site.register(salesOrderdetails)
admin.site.register(PurchaseReturn)
admin.site.register(Purchasereturndetails)

admin.site.register(purchaseorder)
admin.site.register(PurchaseOrderDetails)
admin.site.register(salereturn)
admin.site.register(salereturnDetails)
admin.site.register(journal,journalAdmin)
admin.site.register(Transactions,TransactionsAdmin)
admin.site.register(StockTransactions,StockTransactionAdmin)
admin.site.register(journalmain)
admin.site.register(journaldetails)