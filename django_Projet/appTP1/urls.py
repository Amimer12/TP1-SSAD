from django.urls import path,include
from . import views


urlpatterns = [
        path('Auth_Page/',views.AuthPage),
]
