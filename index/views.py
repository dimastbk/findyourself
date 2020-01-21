from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView

from uuslug import slugify

from .forms import IndexMapForm, PlaceForm
from .models import Place, Route, Type
from .track_file import makeallgpx, makeallkml, makeoncegpx, makeoncekml


class IndexMapJsView(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        query = {k: v for k, v in kwargs.items() if v != '0'}
        query['is_published'] = True
        qs = Place.objects.filter(**query).all()
        resp = serialize(
            'geojson',
            qs,
            geometry_field='coord',
            fields=('pk', 'title', 'type_place'),
        )
        return HttpResponse(f'var place_arr = {resp}', content_type='text/javascript')


@method_decorator(csrf_exempt, name='dispatch')
class IndexMapPageView(FormView):

    title_page = 'Карта мест'
    template_name = 'index/map.html'
    form_class = IndexMapForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_place'] = Type.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data(**{'form': form})
        context['script_url'] = reverse(
            'indexmap_js',
            kwargs={k: v or 0 for k, v in form.data.items()},
        )
        return self.render_to_response(context)


@method_decorator(csrf_exempt, name='dispatch')
class IndexListPageView(FormView):

    title_page = 'Все места'
    template_name = 'index/list.html'
    form_class = IndexMapForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['place_list'] = Place.objects.filter(is_published=True).all()
        return self.render_to_response(context)

    def form_valid(self, form):
        context = self.get_context_data(**{'form': form})
        query = {k: v for k, v in form.cleaned_data.items() if v is not None}
        query['is_published'] = True
        context['place_list'] = Place.objects.filter(**query).all()
        return self.render_to_response(context)


class IndexPageView(TemplateView):

    title_page = 'Главная'
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_places'] = Place.objects.filter(is_published=True).order_by('-pk')[:6]
        return context


class PlaceDetailView(DetailView):

    model = Place

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            pk=self.kwargs['pk'], is_published=True,
        ).select_related('city', 'type_place').prefetch_related('district', 'route_place')
        return qs

    def title_page(self):
        return '{0} ({1})'.format(
            self.get_object().title,
            self.get_object().type_place.title.lower(),
        )


class GetRoute(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        route = Route.objects.select_related('rt_from', 'rt_to').get(pk=self.kwargs['pk'])
        filename = slugify(route.rt_title)
        if self.kwargs['format'] == 'kml':
            response = HttpResponse(
                makeoncekml(route),
                content_type='application/vnd.google-earth.kml+xml',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.kml"'
        elif self.kwargs['format'] == 'gpx':
            response = HttpResponse(
                makeoncegpx(route),
                content_type='application/gpx+xml',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.gpx"'
        else:
            response = HttpResponseBadRequest()
        return response


class GetAllRoute(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        routes = Place.objects.filter(
            pk=self.kwargs['pk'], is_published=True,
        ).prefetch_related('route_place').first()
        filename = slugify(routes.title)
        if self.kwargs['format'] == 'kml':
            response = HttpResponse(
                makeallkml(routes),
                content_type='application/vnd.google-earth.kml+xml',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.kml"'
        elif self.kwargs['format'] == 'gpx':
            response = HttpResponse(
                makeallgpx(routes),
                content_type='application/gpx+xml',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.gpx"'
        else:
            response = HttpResponseBadRequest()
        return response


class PlaceCreateView(LoginRequiredMixin, CreateView):

    model = Place
    form_class = PlaceForm
    title_page = 'Добавить новое место'


class PlaceEditView(LoginRequiredMixin, UpdateView):

    model = Place
    form_class = PlaceForm
    title_page = 'Редактировать место'
