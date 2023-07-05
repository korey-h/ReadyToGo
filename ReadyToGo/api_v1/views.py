from rest_framework.exceptions import PermissionDenied

from registration.models import Participants, Races
from registration.utilities import get_reg_code
from rest_framework import pagination
from rest_framework.viewsets import ModelViewSet

from .filters import active_only_filter
from .serializers import (
    ParticipantSerializer, RaceDetailSerializer, RacesSerializer
    )


class RacesViewSet(ModelViewSet):
    serializer_class = RacesSerializer
    queryset = Races.objects.all()
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size_query_param = 'limit'
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


class RegistrationViewSet(ModelViewSet):
    serializer_class = ParticipantSerializer
    queryset = Participants.objects.all()
    pagination_class = None
    lookup_url_kwarg = 'reg_code'
    lookup_field = 'reg_code'

    @staticmethod
    def _check_race_is_active(serializer):
        d = serializer.validated_data
        if not d['race'].is_active:
            raise PermissionDenied(
                detail='Регистрация на мероприятие прекращена.'
            )

    def perform_create(self, serializer):
        self._check_race_is_active(serializer)
        d = serializer.validated_data
        data = d['race'].name + d['name'] + d['surname'] + d['patronymic']
        reg_code = get_reg_code(data)
        serializer.save(reg_code=reg_code)

    def perform_update(self, serializer):
        self._check_race_is_active(serializer)
        serializer.save()
