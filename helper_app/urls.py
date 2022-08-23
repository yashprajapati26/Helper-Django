from django.urls import path
from helper_app import views

app_name = "helper_app"

urlpatterns = [

    path("",views.index,name="index"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("verifyotp/",views.OtpVerifyView.as_view(),name="verifyotp"),
    path("register/",views.RegisterView.as_view(),name="register"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    

    path("services/",views.ServicesView.as_view(),name="services"),

    path("load_more_service/",views.load_more_service,name="load_more_service"),


    path("maptime/",views.maptime,name="maptime"),
    path("final/",views.final,name="final"),

]
