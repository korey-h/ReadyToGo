from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("signup_done/", views.CustomRegistrationDoneView.as_view(),
         name="signup_done"),  
    path("signup_confirm/<uidb64>/<token>/",
         views.CustomRegistrationConfirmView.as_view(),
         name="signup_confirm"),
]
