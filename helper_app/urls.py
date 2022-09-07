from django.urls import path
from helper_app import views
from django.contrib.auth import views as auth_views 
app_name = "helper_app"

urlpatterns = [

    path("",views.index,name="index"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("verifyotp/",views.OtpVerifyView.as_view(),name="verifyotp"),
    path("register/",views.RegisterView.as_view(),name="register"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("contact/",views.ContactView.as_view(),name="contact"),
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']
    path("password_reset", views.password_reset_request.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Admin/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Admin/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Admin/password_reset_complete.html'), name='password_reset_complete'),

    path("services/",views.ServicesView.as_view(),name="services"),
    path("service-details/<int:pk>/",views.ServiceDetailsView.as_view(),name="service_details"),
    path("show_services/<slug:slug>/",views.ShowServicesView.as_view(),name="show_services"),
    path("load_more_service/",views.load_more_service,name="load_more_service"),

    path("check_location/",views.check_location,name="check_location"),


    path("maptime/",views.maptime,name="maptime"),
    path("final/",views.final,name="final"),

]
