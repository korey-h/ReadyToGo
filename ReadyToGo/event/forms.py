from django import forms

from registration.models import Categories, Cups, Races


class CupForm(forms.ModelForm):

    class Meta():
        model = Cups
        fields = '__all__'


class RaceForm(forms.ModelForm):

    class Meta():
        model = Races
        fields = '__all__'


class CategoryForm(forms.ModelForm):

    class Meta():
        model = Categories
        fields = '__all__'
        widgets = {'race': forms.HiddenInput()}
