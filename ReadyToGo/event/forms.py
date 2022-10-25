from django import forms

from registration.models import Cups


class CupForm(forms.ModelForm):

    class Meta():
        model = Cups
        fields = '__all__'
