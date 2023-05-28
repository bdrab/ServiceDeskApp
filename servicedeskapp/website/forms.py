from django import forms
from incident.models import Category, Incident


# class CategoryForm(forms.Form):
#     Category = forms.ModelChoiceField(queryset=Category.objects.all())

from django.forms import ModelForm


class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = ["category", "description"]
