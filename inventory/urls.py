from django.urls import path
from inventory import views


app_name = 'inventory'

urlpatterns  = [

    path('createProduct',views.CreateTodoApiView.as_view(), name = 'product1'),
    path('ListProduct',views.ListproductApiView.as_view(), name = 'listproduct'),
    path('product',views.productApiView.as_view(), name = 'product'),
    path('<int:id>',views.productupdatedel.as_view(), name = 'product2'),
    path('album',views.AlbumApiView.as_view(), name = 'Album'),
    path('album/<int:id>',views.Albumupdatedel.as_view(), name = 'Album2'),
    path('track',views.TrackApiView.as_view(), name = 'Track'),
    path('<int:id>',views.TrackApiView.as_view(), name = 'track2'),
    
   
] 