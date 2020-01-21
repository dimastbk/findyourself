from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.core.validators import RegexValidator
from django.urls import reverse

import srtm
from imagefield.fields import ImageField
from taggit.managers import TaggableManager

from .mixin import CoordMixin


class Place(models.Model, CoordMixin):

    title = models.CharField(max_length=200, verbose_name='Название')
    title_alt = models.CharField(
        max_length=200,
        verbose_name='Альтернативное название',
        blank=True,
        help_text='Другое распространённое название, иногда официальное название на картах. '
        + 'Например, Литовка для горы Фалаза.',
    )
    text = models.TextField(verbose_name='Описание')
    image = ImageField(blank=True, auto_add_fields=True, verbose_name='Изображение')
    type_place = models.ForeignKey(
        'Type', on_delete=models.SET_NULL, null=True, verbose_name='Категория',
    )

    wd_id = models.CharField(
        blank=True,
        max_length=10,
        verbose_name='ID на Wikidata',
        help_text='Например, Q4317189 для '
        + '<a href="https://www.wikidata.org/wiki/Q4317189">водопад Неожиданный</a>.',
        validators=[RegexValidator(regex='^Q([0-9]{1,9})$')],
    )
    ig_id = models.CharField(
        blank=True,
        max_length=20,
        verbose_name='Локация в Инстаграме',
        help_text='Например, 771936715 для '
        + '<a href="https://www.instagram.com/explore/locations/771936715/">гора Ольховая</a>.',
    )
    coord = models.PointField(blank=True, null=True, verbose_name='Координаты')

    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Населённый пункт',
        help_text='Ближайший населённый пункт с которого начинаются основные маршруты.',
    )
    district = models.ManyToManyField('District', verbose_name='Район')
    region = models.ForeignKey(
        'Region', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Регион',
    )

    tags = TaggableManager(blank=True)

    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('place', kwargs={'pk': self.id})

    def get_ig_link(self):
        if self.ig_id:
            return f'https://www.instagram.com/explore/locations/{self.ig_id}/'

    def get_wd_link(self):
        if self.wd_id:
            return f'https://www.wikidata.org/wiki/Special:GoToLinkedPage/ruwiki/{self.wd_id}'


class Type(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_pl = models.CharField(max_length=200, verbose_name='Множественное название')
    icon = models.CharField(max_length=200, verbose_name='Название иконки')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class City(models.Model, CoordMixin):
    title = models.CharField(max_length=200, verbose_name='Название')

    ae1 = models.ForeignKey(
        'District', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Район',
    )
    ae2 = models.ForeignKey(
        'Region', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Регион',
    )

    wd_id = models.CharField(max_length=10)
    coord = models.PointField(blank=True, null=True, verbose_name='Координаты')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['title']

    def __str__(self):
        return self.title


class District(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    capital = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Центр')
    region = models.ForeignKey(
        'Region', on_delete=models.SET_NULL, null=True, verbose_name='Регион',
    )
    wd_id = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Region(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    capital = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Центр')
    wd_id = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Route(models.Model, CoordMixin):

    status = (
        ('w', 'Водный'),
        ('a', 'Автомобильный'),
        ('h', 'Пеший'),
    )

    rt_title = models.CharField(max_length=200, verbose_name='Название')
    rt_from = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Начальный пункт',
        related_name='route_city',
    )
    rt_to = models.ForeignKey(
        'Place',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Конечный пункт',
        related_name='route_place',
    )
    rt_type = models.CharField(
        max_length=1, choices=status, blank=True, default='h', verbose_name='Тип маршрута',
    )
    ls = models.LineStringField(blank=True, null=True, srid=4326, dim=3, verbose_name='Маршрут')
    ls2 = models.LineStringField(blank=True, null=True, srid=4326, dim=2, verbose_name='2D-маршрут')
    rt_length = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=2, verbose_name='Длина',
    )
    rt_max_el = models.DecimalField(
        blank=True, null=True, max_digits=6, decimal_places=2, verbose_name='Максимальная высота',
    )
    rt_min_el = models.DecimalField(
        blank=True, null=True, max_digits=6, decimal_places=2, verbose_name='Минимальная высота',
    )
    rt_el_gain = models.DecimalField(
        blank=True, null=True, max_digits=7, decimal_places=2, verbose_name='Набор высоты',
    )
    rt_el_loss = models.DecimalField(
        blank=True, null=True, max_digits=7, decimal_places=2, verbose_name='Потеря высоты',
    )
    rt_is_gpx = models.BooleanField(default=False, verbose_name='GPX?')

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f'{self.rt_from} - {self.rt_to}'

    def get_absolute_url(self):
        return reverse('place', kwargs={'pk': self.rt_to.pk})

    def save(self, *args, **kwargs):
        elevation_data = srtm.get_data()
        max_el, min_el, el_gain, el_loss, el, last_el = 0, 9999, 0, 0, 0, None
        coord_list, ls = [], False

        # todo: возможно, есть разные случаи, нужно больше тестов

        # если gpx (ставится в обработчике формы), то проверяем наличие высоты
        if self.rt_is_gpx and hasattr(self, 'coords'):
            ls = LineString(self.coords, srid=4326)
            # уменьшаем количество точек в треке
            # вероятно, нужно это делать до подсчёта высоты и длины, ибо данные получаются неверными 
            ls = ls.simplify(tolerance=0.00001)
            # если высота отсутствует, то копируем в 2D и убираем флаг GPX
            if not ls.hasz:
                self.ls2 = ls
                self.rt_is_gpx = False

        # если есть плоские коордиинаты, то считаем высоту из SRTM
        if not self.rt_is_gpx and self.ls2:
            for p in self.ls2.coords:
                # Добавляем высоту
                el = elevation_data.get_elevation(p[1], p[0])
                coord_list.append((p[0], p[1], el))

                ls = LineString(coord_list, srid=4326)

        # иначе забиваем ls2, убирая высоту (нужно для виджета leaflet)
        else:
            self.ls2 = LineString(
                [(p[0], p[1]) for p in ls.coords],
                srid=4326,
            )

        # если есть линия, то начинаем считать высоты и потери
        if ls:
            for pnt in ls.coords:
                el = pnt[2]

                # Максимальная/минимальная высота
                max_el = el if el > max_el else max_el
                min_el = el if el < min_el else min_el

                # Вычисляем набор/потерю высоты
                if last_el:
                    if (el - last_el) > 0:
                        el_gain += el - last_el
                    else:
                        el_loss -= el - last_el

                last_el = el

            self.ls = ls
            self.rt_el_gain = el_gain
            self.rt_el_loss = el_loss
            self.rt_max_el = max_el
            self.rt_min_el = min_el

            # считаем зону UTM для корректного расчёта длины
            # ls.centroid.x - долгота центра маршрута
            zone = 32660 - round((177 - ls.centroid.x) / 6)
            ls.transform(zone)

            # Считаем длину маршрута
            self.rt_length = ls.length / 1000

        super().save(*args, **kwargs)
