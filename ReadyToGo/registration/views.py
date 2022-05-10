from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView

from .forms import RegForm
from .models import Cups, Races
from .utilities import find_slug


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
        slug = find_slug(self.request.path, 'race/', '/registration')
        obj = get_object_or_404(Races, slug=slug)
        kwargs.update({'obj': obj})
        self.initial.update({'race': obj})
        return super().get_context_data(**kwargs)

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        return form
