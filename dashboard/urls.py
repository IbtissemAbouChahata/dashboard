from django.urls import path
from . import views

urlpatterns =[
    path("dashboard/",views.fetch_data,name="app-index"),
     path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('detection/', views.defdetect, name='detection'),
    path('addvalue/', views.add_value, name='addvalue'),
    path('signup/', views.signup, name='signup'),
     path('latest/', views.fetch_latest_value, name='get_latest_value'),
    
]