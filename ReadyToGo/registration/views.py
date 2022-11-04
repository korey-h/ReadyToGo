from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import RaceFilterForm, RegEditForm, RegForm
from .models import Participants, Races
from .utilities import get_reg_code


def index(request):
    params = {}
    form = RaceFilterForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        from_time = data['from_time']
        to_time = data['to_time']
        if data['cup']:
            params.update({'cup_id': data['cup']})
        if from_time and to_time:
            params.update(
                {'date__range': (from_time, to_time)}
            )
        elif from_time:
            params.update({'date__gte': from_time})
        elif to_time:
            params.update({'date__lte': to_time})

    races = Races.objects.filter(**params).order_by('date')
    paginator = Paginator(races, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'filter_form': form})


def race_info(request, slug):
    race = get_object_or_404(Races, slug=slug)
    return render(request, 'race_info.html', {'race': race})


def race_participants(request, slug):
    race = get_object_or_404(Races, slug=slug)
    return render(request, 'participants.html',
                  {'race': race, 'participants': race.race_participants.all()})


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


class RegView(CreateView, UpdateView, ):
    model = Participants
    form_class = RegForm
    template_name = 'reg_form.html'

    def get_form(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        race = Races.objects.get(slug=slug)
        self.initial.update({'race': race})
        return super().get_form(*args, **kwargs)

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('race_participants', kwargs={'slug': slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        slug = self.kwargs['slug']
        url = reverse('race_registration', kwargs={'slug': slug})
        if self.request.path == url:
            obj = self.object
            data = obj.race.name + obj.name + obj.surname + obj.patronymic
            obj.reg_code = get_reg_code(data)
            redirect = render(
                self.request, 'success_reg.html',
                {'participant': obj, 'race': obj.race})
        else:
            redirect = HttpResponseRedirect(self.get_success_url())
        self.object.save()
        return redirect

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get(self.slug_url_kwarg)
        url = reverse('race_registration', kwargs={'slug': slug})
        if self.request.path == url:
            return None

        pk = self.kwargs.get(self.pk_url_kwarg)
        url = reverse('participant_selfupdate',
                      kwargs={'slug': slug, 'pk': pk})
        if self.request.path == url:
            return get_object_or_404(self.model, reg_code=pk)
        return super().get_object(*args, **kwargs)


class DelRegView(DeleteView):
    model = Participants
    slug_field = None
    template_name = None

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('race_participants', kwargs={'slug': slug})
