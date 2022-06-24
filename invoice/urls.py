from django.urls import path
from invoice import views


app_name = 'invoice'

urlpatterns  = [

   
    path('salesorder',views.SalesOderHeaderApiView.as_view(),name = 'salesorder'),
    path('salesorder/<int:id>',views.salesOrderupdatedelview.as_view(), name = 'salesorder'),
    path('salesorderdetails',views.salesOrderdetailsApiView.as_view(),name = 'salesorder'),
    path('salesorderdetails/<int:id>',views.salesOrderdetailsApiView.as_view(), name = 'salesorder'),
    path('purchaseorder',views.purchaseorderApiView.as_view(),name = 'purchaseorder'),
    path('purchaseorder/<int:id>',views.purchaseorderupdatedelview.as_view(), name = 'purchaseorder'),
    path('purchaseorderdetails',views.PurchaseOrderDetailsApiView.as_view(),name = 'purchaseorder'),
    path('purchaseorderdetails/<int:id>',views.purchaseorderupdatedelview.as_view(), name = 'purchaseorder'),
    path('voucherno',views.purchaseordelatestview.as_view(), name = 'purchaseorder'),
    path('billno',views.salesorderlatestview.as_view(), name = 'purchaseorder'),
    path('journal',views.JournalApiView.as_view(), name = 'journal'),
    path('srvoucherno',views.salesreturnlatestview.as_view(), name = 'journal'),
    path('salesreturn',views.salesreturnApiView.as_view(), name = 'journal'),
    path('salesreturn/<int:id>',views.salesreturnupdatedelview.as_view(), name = 'journal'),
    path('jvouccherno',views.journalordelatestview.as_view(), name = 'purchaseorder'),

    
    # path('account',views.accountApiView.as_view(),name ='account'),
    # path('account/<int:id>',views.accountupdatedelApiView.as_view(),name = 'accountid')
   
   
   
] 