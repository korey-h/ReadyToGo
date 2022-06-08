from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import RegForm
from .models import Cups, Participants, Races


def index(request):
    races = Races.objects.all().order_by('date')
    paginator = Paginator(races, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def race_info(request, slug):
    race = get_object_or_404(Races, slug=slug)
    return render(request, 'race_info.html', {'race': race})


def race_participants(request, slug):
    race = get_object_or_404(Races, slug=slug)
    return render(request, 'participants.html',
                  {'race': race, 'participants': race.race_participants.all()})


def cup_info(request, slug):
    cup = get_object_or_404(Cups, slug=slug)
    return render(request, 'cup_info.html',
                  {'cup': cup, 'races': cup.cup_races.all()})


class RegView(CreateView):
    form_class = RegForm
    template_name = 'reg_form.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        race = Races.objects.get(slug=slug)
        self.initial.update({'race': race})
        kwargs.update({'race': race})
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('race_participants', kwargs={'slug': slug})


class DelRegView(DeleteView):
    model = Participants
    slug_field = None
    template_name = None

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('race_participants', kwargs={'slug': slug})


class UpdRegView(UpdateView):
    model = Participants
    slug_field = None
    form_class = RegForm
    template_name = 'reg_form.html'

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('race_participants', kwargs={'slug': slug})

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        race = Races.objects.get(slug=slug)
        self.initial.update({'race': race})
        kwargs.update({'race': race})
        return super().get_context_data(**kwargs)
