from django import forms
from django.conf import settings
import datetime



class TripForm(forms.Form):
    starting_destination = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Where From?'}))
    final_destination = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Where To?'}))
    #date_start = forms.DateField(widget = forms.SelectDateWidget)
    #date_end = forms.DateField(widget = forms.SelectDateWidget)
    date_start = forms.DateField()
    #date_end = forms.DateField()

    def clean_date_start(self):
        date = self.cleaned_data['date_start']
        if date<datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date cannot be in the past!")
        return date

    def clean_final_destination(self):
        destination = self.cleaned_data['final_destination']
        start=self.cleaned_data['starting_destination']
        if(destination==start):
            raise forms.ValidationError("The destination address cannot be the same as the start address!")
        return destination