from django.urls import path

from . import views

urlpatterns = [
    path("cup/info/<slug:slug>/", views.cup_info, name="cup_info"),
    path("cup/create/", views.CupView.as_view(), name="cup_create"),
    path("cup/update/<slug:slug>/", views.CupView.as_view(),
         name="cup_update"),
    path("cup/delete/<slug:slug>/", views.DelCupView.as_view(),
         name="cup_delete"),
]
