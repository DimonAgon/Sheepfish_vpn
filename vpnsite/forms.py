
from django import forms

from vpnsite.models import Site


class AddSiteForm(forms.Form):
    url = forms.CharField(#TODO: change to URLfield, configure localhost url checking
        label="url",
        widget=forms.URLInput(
            attrs={'class': "field", 'autofocus': True}
        )
    )

    name = forms.CharField(
        label="name",
        widget=forms.TextInput(
            attrs={'class': "field"}
        )
    )
