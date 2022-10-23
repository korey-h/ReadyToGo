from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import RegForm, RegEditForm
from .models import Cups, Participants, Races
from .utilities import get_reg_code


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


def enter_edit_reg_info(request, slug):
    form = RegEditForm()
    if request.method == "POST":
        form = RegEditForm(request.POST)
        if form.is_valid():
            reg_code = form.cleaned_data['reg_code']
            return HttpResponseRedirect(
                reverse('participant_selfupdate',
                        kwargs={'slug': slug, 'pk': reg_code}))
    race = get_object_or_404(Races, slug=slug)
    return render(request, "entr_edit_form.html", {"form": form, 'race': race})


class RegView(CreateView):
    form_class = RegForm
    template_name = 'reg_form.html'

    def get_form(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        race = Races.objects.get(slug=slug)
        self.initial.update({'race': race})
        return super().get_form(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        obj = self.object
        data = obj.race.name + obj.name + obj.surname + obj.patronymic
        obj.reg_code = get_reg_code(data)
        obj.save()
        return render(self.request, 'success_reg.html',
                      {'participant': obj, 'race': obj.race})


class DelRegView(DeleteView):
    model = Participants
    slug_field = None
    template_name = None

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('race_participants', kwargs={'slug': slug})


class UpdRegView(UpdateView):
    model = Participants
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

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        url = reverse('participant_selfupdate',
                      kwargs={'slug': slug, 'pk': pk})
        if self.request.path == url:
            return get_object_or_404(self.model, reg_code=pk)
        return super().get_object(*args, **kwargs)
