from django import forms

import gpxpy
from gpxpy import gpx as mod_gpx
from leaflet.forms.widgets import LeafletWidget

from .mixin import CssClassFormMixin
from .models import District, Place, Region, Route, Type


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
            'title',
            'title_alt',
            'text',
            'image',
            'type_place',
            'wd_id',
            'ig_id',
            'coord',
            'city',
            'district',
            'region',
        )
        widgets = {
            'coord': LeafletWidget(),
            'text': forms.Textarea(attrs={'rows': 3}),
        }


class RouteForm(CssClassFormMixin, forms.ModelForm):

    gpx_file = forms.FileField(required=False, label='Трек в формате GPX')

    class Meta:
        model = Route
        fields = (
            'rt_title',
            'rt_type',
            'rt_from',
            'rt_to',
            'ls2',
        )
        widgets = {
            'ls2': LeafletWidget(),
        }

    def clean_gpx_file(self):
        gpx_file = self.cleaned_data.get('gpx_file')
        if gpx_file:
            gpx_file = gpx_file.read().decode('utf-8')
            coords = []
            try:
                gpx = gpxpy.parse(gpx_file)
                for segment in gpx.tracks[0].segments:
                    coords.extend([(p.longitude, p.latitude, p.elevation) for p in segment.points])
                return coords
            except (mod_gpx.GPXXMLSyntaxException, mod_gpx.GPXException) as e:
                raise forms.ValidationError(e)
            except IndexError:
                raise forms.ValidationError('В GPX файле отсутствуют треки.')

    def save(self, commit=True):
        route = super().save(commit=False)
        gpx_coord = self.cleaned_data.get('gpx_file')

        if gpx_coord:
            route.rt_is_gpx = True
            route.coords = gpx_coord

        if commit:
            route.save()

        return route
