from django.urls import path

from . import views


urlpatterns = [
    path('races/', views.RacesViewSet.as_view({'get': 'list'})),
    path('races/<int:id>/', views.RacesViewSet.as_view({'get': 'retrieve'})),  
]
