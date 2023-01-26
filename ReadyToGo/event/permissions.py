from django.contrib.auth.mixins import PermissionRequiredMixin


class MakerRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        user = self.request.user
        obj = self.get_object()
        if obj:
            return user.is_superuser or (user == obj.maker)
        return True
