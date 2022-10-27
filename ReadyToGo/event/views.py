from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from registration.models import Categories, Cups, Races

from .forms import CategoryForm, CupForm, RaceForm
from .utilities import create_def_category


def cup_info(request, slug):
    cup = get_object_or_404(Cups, slug=slug)
    return render(request, 'cup_info.html',
                  {'cup': cup, 'races': cup.cup_races.all()})


def get_all_cups(request):
    cups = Cups.objects.all()
    paginator = Paginator(cups, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'cups_all.html', {'page': page})


class CupView(CreateView, UpdateView, ):
    model = Cups
    form_class = CupForm
    template_name = 'cup_create_form.html'

    def get_success_url(self):
        url = reverse('cup_create')
        if self.request.path == url:
            return reverse('all_cups')
        slug = self.kwargs['slug']
        return reverse('cup_info', kwargs={'slug': slug})

    def get_object(self, *args, **kwargs):
        url = reverse('cup_create')
        if self.request.path == url:
            return None
        return super().get_object(*args, **kwargs)


class DelCupView(DeleteView):
    model = Cups

    def get_success_url(self):
        return reverse('all_cups')


class RaceView(CreateView, UpdateView, ):
    model = Races
    form_class = RaceForm
    template_name = 'race_create_form.html'

    def get_success_url(self):
        url = reverse('race_create')
        if self.request.path == url:
            return reverse('index')
        slug = self.kwargs['slug']
        return reverse('race_info', kwargs={'slug': slug})

    def get_object(self, *args, **kwargs):
        url = reverse('race_create')
        if self.request.path == url:
            return None
        return super().get_object(*args, **kwargs)

    def form_valid(self, form):
        result = super().form_valid(form)
        create_def_category(self.object, CategoryForm)
        return result


class DelRaceView(DeleteView):
    model = Races

    def get_success_url(self):
        return reverse('index')


class CategoryView(CreateView, UpdateView, ):
    model = Categories
    form_class = CategoryForm
    template_name = 'cat_create_form.html'

    def get_form(self, *args, **kwargs):
        slug = self.kwargs.get('race_slug')
        race = Races.objects.get(slug=slug)
        self.initial.update({'race': race})
        return super().get_form(*args, **kwargs)

    def get_success_url(self):
        slug = self.kwargs['race_slug']
        return reverse('race_update', kwargs={'slug': slug})

    def get_object(self, *args, **kwargs):
        race = self.kwargs['race_slug']
        url = reverse('category_create', kwargs={'race_slug': race})
        if self.request.path == url:
            return None

        slug = self.kwargs['slug']
        return get_object_or_404(Categories, slug=slug, race__slug=race)


class DelCategoryView(DeleteView):
    model = Categories

    def get_object(self, *args, **kwargs):
        race_slug = self.kwargs['race_slug']
        slug = self.kwargs['slug']
        return get_object_or_404(Categories, slug=slug, race__slug=race_slug)

    def get_success_url(self):
        slug = self.kwargs['race_slug']
        return reverse('race_update', kwargs={'slug': slug})