from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from registration.models import Categories, Cups, Races
from registration.utilities import DefCategory

from .forms import CategoryForm, CupForm, RaceForm


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


def race_by_template(request):
    if request.method == 'POST':
        race_slug = request.POST.get('race_slug')
        query = Races.objects.filter(slug=race_slug)
        if query:
            race_data = query.values()[0]
            race_data.pop('id')
            race_data.pop('slug')
            race_data['name'] = 'copy_' + race_data['name']
            new = Races.objects.create(**race_data)

            race_categories = query[0].race_categories.all()
            for cat in race_categories.values():
                cat.pop('id')
                cat['race_id'] = new.id
                Categories.objects.create(**cat)

            return HttpResponseRedirect(
                reverse('race_update', kwargs={'slug': new.slug})
            )

    return HttpResponseRedirect(reverse('race_create'))


class CupView(LoginRequiredMixin, CreateView, UpdateView, ):
    model = Cups
    form_class = CupForm
    template_name = 'cup_create_form.html'

    def get_success_url(self):
        url = reverse('cup_create')
        if self.request.path == url:
            return reverse('all_cups')
        slug = self.object.slug
        return reverse('cup_info', kwargs={'slug': slug})

    def get_object(self, *args, **kwargs):
        url = reverse('cup_create')
        if self.request.path == url:
            return None
        return super().get_object(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.object.id:
            self.object.maker = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DelCupView(LoginRequiredMixin, DeleteView):
    model = Cups

    def get_success_url(self):
        return reverse('all_cups')


class RaceView(LoginRequiredMixin, CreateView, UpdateView, ):
    model = Races
    form_class = RaceForm
    template_name = 'race_create_form.html'

    def get_success_url(self):
        url = reverse('race_create')
        if self.request.path == url:
            return reverse('index')
        slug = self.object.slug
        return reverse('race_info', kwargs={'slug': slug})

    def get_object(self, *args, **kwargs):
        url = reverse('race_create')
        if self.request.path == url:
            return None
        return super().get_object(*args, **kwargs)

    def form_valid(self, form):
        result = super().form_valid(form)
        url = reverse('race_create')
        if self.request.path == url:
            DefCategory.create(self.object, Categories)
        return result


class DelRaceView(LoginRequiredMixin, DeleteView):
    model = Races

    def get_success_url(self):
        return reverse('index')

    def delete(self, request, *args, **kwargs):
        """Предварительное удаление связанных Categories.
        Иначе set_def_category мешает
        """
        self.object = self.get_object()
        self.object.race_categories.exclude(slug=DefCategory.slug).delete()

        # непосредственное удаление Race
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class CategoryView(LoginRequiredMixin, CreateView, UpdateView, ):
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


class DelCategoryView(LoginRequiredMixin, DeleteView):
    model = Categories

    def get_object(self, *args, **kwargs):
        race_slug = self.kwargs['race_slug']
        slug = self.kwargs['slug']
        return get_object_or_404(Categories, slug=slug, race__slug=race_slug)

    def get_success_url(self):
        slug = self.kwargs['race_slug']
        return reverse('race_update', kwargs={'slug': slug})
