from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from registration.models import Races


class MakerRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        user = self.request.user
        if user.is_superuser:
            return True

        obj = self.get_object()
        if obj:
            return user == obj.maker

        race_slug = self.kwargs.get('race_slug')
        if race_slug:
            race = get_object_or_404(Races, slug=race_slug)
            return user == race.maker

        return True
