from django import forms

from leaflet.forms.widgets import LeafletWidget

from .mixin import CssClassFormMixin
from .models import District, Place, Region, Type


class IndexMapForm(CssClassFormMixin, forms.Form):
    type_place = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        empty_label='Все категории',
        required=False,
        widget=forms.Select(),
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        empty_label='Все районы',
        required=False,
        widget=forms.Select(),
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label='Все регионы',
        required=False,
        widget=forms.Select(),
    )


class PlaceForm(CssClassFormMixin, forms.ModelForm):

    class Meta:
        model = Place
        fields = (
            'title', 'title_alt', 'text', 'image', 'type_place',
            'wd_id', 'ig_id', 'coord', 'city', 'district', 'region',
        )
        widgets = {
            'coord': LeafletWidget(),
            'text': forms.Textarea(attrs={
                'rows': 3,
            }),
        }
