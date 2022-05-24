from django.urls import path
from geography import views


app_name = 'geography'

urlpatterns  = [

   
    path('country',views.countryApiView.as_view(),name = 'country'),
    path('country/<int:id>',views.countryApiView.as_view(), name = 'countryid'),
    path('state', views.stateApiView.as_view() ,name = 'state'),
    path('state/<int:id>',views.stateApiView.as_view(), name = 'stateid'),
    path('district',views.districtApiView.as_view(),name = 'district'),
    path('district/<int:id>',views.districtApiView.as_view(), name = 'districtid'),
    path('city', views.cityApiView.as_view() ,name = 'city'),
    path('city/<int:id>',views.cityApiView.as_view(), name = 'cityid'),
   
   
   
    
   
] 