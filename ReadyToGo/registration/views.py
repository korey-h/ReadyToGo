from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Races


def index(request):
    races = Races.objects.all().order_by('date')
    paginator = Paginator(races, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def race_info(request, slug):
    race = get_object_or_404(Races, slug=slug)
    return render(request, 'race_info.html', {'race': race})
