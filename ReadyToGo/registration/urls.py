from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("race/<slug:slug>/", views.race_info, name="race_info"),
    path("race/<slug:slug>/participants/", views.race_participants,
         name="race_participants"),
    path("cup/<slug:slug>/", views.cup_info, name="cup_info"),
]
