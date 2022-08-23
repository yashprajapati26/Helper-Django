from django.urls import path
from vendor_app import views

app_name = "vendor_app"

urlpatterns = [

    path("",views.HomeView.as_view(),name="home"),
    path("addservice/",views.AddServiceView.as_view(),name="addservice"),
   
]
