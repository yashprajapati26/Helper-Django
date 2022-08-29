from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI


urlpatterns = [
    path('test_api/register/', RegisterAPI.as_view(), name='register'),


    path('test_api/login/', LoginAPI.as_view(), name='login'),
    path('test_api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('test_api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]