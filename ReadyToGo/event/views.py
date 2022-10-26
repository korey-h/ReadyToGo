from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from registration.models import Cups

from .forms import CupForm


def cup_info(request, slug):
    cup = get_object_or_404(Cups, slug=slug)
    return render(request, 'cup_info.html',
                  {'cup': cup, 'races': cup.cup_races.all()})


class CupView(CreateView, UpdateView, ):
    model = Cups
    form_class = CupForm
    template_name = 'cup_create_form.html'

    def get_success_url(self):
        url = reverse('cup_create')
        if self.request.path == url:
            return reverse('index')
        slug = self.kwargs['slug']
        return reverse('cup_info', kwargs={'slug': slug})

    def get_object(self, *args, **kwargs):
        url = reverse('cup_create')
        if self.request.path == url:
            return None
        return super().get_object(*args, **kwargs)


class DelCupView(DeleteView):
    model = Cups
    slug_field = None
    template_name = None

    def get_success_url(self):
        return reverse('index')

    def get_object(self, *args, **kwargs):
        slug = self.kwargs['slug']
        return get_object_or_404(Cups, slug=slug)

