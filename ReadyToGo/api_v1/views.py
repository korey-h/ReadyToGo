from registration.models import Races
from rest_framework.viewsets import ModelViewSet

from .filters import active_only_filter
from .serializers import RacesSerializer, RaceDetailSerializer


class RacesViewSet(ModelViewSet):
    serializer_class = RacesSerializer
    queryset = Races.objects.all()
    pagination_class = None
    cust_filters = [active_only_filter]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        queryset = self.queryset
        for filter in self.cust_filters:
            queryset = filter(queryset, self.request)
        return queryset

    def get_serializer_class(self):
        if self.kwargs.get('id'):
            return RaceDetailSerializer
        return super().get_serializer_class()
