from django import forms
from django.conf import settings


class TripForm(forms.Form):
    starting_destination = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Where From?'}))
    final_destination = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Where To?'}))
    #date_start = forms.DateField(widget = forms.SelectDateWidget)
    #date_end = forms.DateField(widget = forms.SelectDateWidget)
    date_start = forms.DateField()
    #date_end = forms.DateField()