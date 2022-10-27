from django.urls import path

from . import views

urlpatterns = [
    path("cup/all/", views.get_all_cups, name="all_cups"),
    path("cup/info/<slug:slug>/", views.cup_info, name="cup_info"),
    path("create/cup/", views.CupView.as_view(), name="cup_create"),
    path("cup/update/<slug:slug>/", views.CupView.as_view(),
         name="cup_update"),
    path("cup/delete/<slug:slug>/", views.DelCupView.as_view(),
         name="cup_delete"),

    path("create/race/", views.RaceView.as_view(), name="race_create"),
    path("race/update/<slug:slug>/", views.RaceView.as_view(),
         name="race_update"),
    path("race/delete/<slug:slug>/", views.DelRaceView.as_view(),
         name="race_delete"),

    path("create/category/<slug:race_slug>/", views.CategoryView.as_view(),
         name="category_create"),
    path("category/<slug:race_slug>/update/<slug:slug>/",
         views.CategoryView.as_view(),
         name="category_update"),
    path("category/<slug:race_slug>/delete/<slug:slug>/",
         views.DelCategoryView.as_view(),
         name="category_delete"),
]
