from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Cups, Races


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
