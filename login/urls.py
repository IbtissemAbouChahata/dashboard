from django.urls import path
from . import views
urlpatterns = [
    path('login', views.login, name='login_and_fetch_data'),
    path('signup', views.signup, name='sign_up'),
]