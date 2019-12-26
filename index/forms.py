from django import forms

from .models import District, Region, Type


class IndexMapForm(forms.Form):
    type_place = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        empty_label='Все категории',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        empty_label='Все районы',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label='Все регионы',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
