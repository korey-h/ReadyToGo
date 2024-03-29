from django import forms
from registration.models import Categories, Cups, Races


class CupForm(forms.ModelForm):

    class Meta():
        model = Cups
        exclude = ['maker', ]


class RaceForm(forms.ModelForm):

    class Meta():
        model = Races
        exclude = ['maker', ]


class CategoryForm(forms.ModelForm):

    class Meta():
        model = Categories
        exclude = ['maker', ]
        widgets = {'race': forms.HiddenInput()}
