from django.urls import path

from . import views

urlpatterns = [
    path('races/', views.RacesViewSet.as_view({'get': 'list'})),
    path('races/<int:id>/', views.RacesViewSet.as_view({'get': 'retrieve'})),
    path('registration/', views.RegistrationViewSet.as_view(
        {'post': 'create', }
        )),
    path('registration/<reg_code>', views.RegistrationViewSet.as_view(
        {'get': 'retrieve', 'put': 'update'}
        )),
]
