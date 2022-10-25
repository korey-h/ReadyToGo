from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("race/<slug:slug>/", views.race_info, name="race_info"),
    path("race/<slug:slug>/participants/", views.race_participants,
         name="race_participants"),
    path("race/<slug:slug>/participants/<int:pk>/delete/",
         views.DelRegView.as_view(),
         name="delete_participant"),
    path("race/<slug:slug>/participants/self_update/<str:pk>/",
         views.RegView.as_view(), name="participant_selfupdate"),
    path("race/<slug:slug>/participants/<int:pk>/update/",
         views.RegView.as_view(),
         name="update_participant"),
    path("race/<slug:slug>/registration/", views.RegView.as_view(),
         name="race_registration"),
    path("race/<slug:slug>/edit_reg_info/", views.enter_edit_reg_info,
         name="edit_reg_info"),
]
