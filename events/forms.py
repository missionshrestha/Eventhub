from django import forms
from . import models
class SearchForm(forms.Form):

    address = forms.CharField(initial="Anywhere")
    city = forms.CharField(initial="Anywhere")
    event_type = forms.ModelChoiceField(required=False,empty_label="Any Kind", queryset=models.EventType.objects.all())
    price = forms.IntegerField(required=False)
    super_organizer = forms.BooleanField(required=False)
    

