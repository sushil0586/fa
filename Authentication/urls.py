from Authentication import views
from django.urls import path

app_name = 'Authentication'

urlpatterns  = [

    path('register',views.RegisterApiView.as_view(), name = 'register'),
    path('login',views.LoginApiView.as_view(), name = 'login'),
    path('user',views.AuthApiView.as_view(), name = 'user'),
]