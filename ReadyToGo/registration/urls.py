from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("race/<slug:slug>/", views.race_info, name="race_info"),
]
