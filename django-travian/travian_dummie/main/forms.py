from socket import fromshare
from django import forms

# This creates forms, which will be mapped in HTML as 'widgets'

class CreateNewVillage(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    number = forms.IntegerField(max_value=1000000)
