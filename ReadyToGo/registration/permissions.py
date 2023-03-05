from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse


class MakerRequiredMixin(PermissionRequiredMixin):
    def get_white_urls(self) -> list:
        white_urls = []
        slug = self.kwargs.get(self.slug_url_kwarg)
        pk = self.kwargs.get(self.pk_url_kwarg)
        url = reverse('participant_selfupdate',
                      kwargs={'slug': slug, 'pk': pk})
        white_urls.append(url)
        return white_urls

    def has_permission(self):
        user = self.request.user
        url = self.request.path
        obj = self.get_object()
        if obj:
            maker = obj.race.maker
            return url in self.get_white_urls() or (
                user.is_superuser or (user == maker)
                )
        return True
