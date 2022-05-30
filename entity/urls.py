from django.urls import path
from entity import views


app_name = 'entity'

urlpatterns  = [

    path('entityadd',views.entityAddApiView.as_view(),name = 'entityadd'),
    path('entity',views.entityApiView.as_view(),name = 'entity'),
    path('entitylist',views.entityApiView.as_view(),name = 'entitylist'),
    path('entity/<int:id>',views.entityupdatedel.as_view(), name = 'entity1'),
    #path('album/<int:id>',views.Albumupdatedel.as_view(), name = 'Album2'),
    path('entityDetails', views.entityDetailsApiView.as_view() ,name = 'entityDetails'),
    path('entityDetails/<int:id>',views.entityDetailsApiView.as_view(), name = 'entityDetails1'),
    path('unittype', views.unitTypeApiView.as_view() ,name = 'unittype'),
    path('unittype/<int:id>',views.unitTypeApiView.as_view(), name = 'unittypeid'),
    # path('entityuser', views.entityUserApiView.as_view() ,name = 'unittype'),
    # path('entityuser/<int:id>',views.entityUserApiView.as_view(), name = 'unittypeid'),
    # path('entityuseradd', views.entityUseraddApiView .as_view() ,name = 'unittype'),
   
   
    
   
] 