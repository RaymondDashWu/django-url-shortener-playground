from django import forms

class URL_Field(forms.Form):
    url = forms.URLField(label="Enter the URL you would like to shorten")