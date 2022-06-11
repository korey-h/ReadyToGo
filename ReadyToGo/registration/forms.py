from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model

from .models import Participants

User = get_user_model()


class CategoryChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        name = obj.name
        race = obj.race.name
        date = datetime.strftime(obj.race.date, '%m.%Y')
        return '_'.join((name, race, date))


class RegForm(forms.ModelForm):

    class Meta():
        model = Participants
        fields = '__all__'
        exclude = ['race']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        participant = kwargs['instance']
        if participant is None:
            race = self.initial['race']
        else:
            race = participant.race
        self.instance.race = race
        queryset = self.fields['category'].queryset.filter(race=race)
        self.fields['category'].queryset = queryset
