from django import forms

from registration.models import Cups, Races


class CupForm(forms.ModelForm):

    class Meta():
        model = Cups
        fields = '__all__'


class RaceForm(forms.ModelForm):

    class Meta():
        model = Races
        fields = '__all__'
