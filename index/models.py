import srtm
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.urls import reverse
from imagefield.fields import ImageField
from taggit.managers import TaggableManager

from .mixin import CoordMixin


class Place(models.Model, CoordMixin):

    title = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    image = ImageField(blank=True, auto_add_fields=True, verbose_name='Изображение')
    type_place = models.ForeignKey(
        'Type',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    wd_id = models.CharField(blank=True, max_length=10)
    ig_id = models.CharField(blank=True, max_length=20, verbose_name='Локация в IG')
    coord = models.PointField(blank=True, null=True, verbose_name='Координаты')

    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Населённый пункт',
    )
    district = models.ManyToManyField('District', verbose_name='Район')
    region = models.ForeignKey(
        'Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Регион',
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
        'District',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Район',
    )
    ae2 = models.ForeignKey(
        'Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Регион',
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
    capital = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Центр',
    )
    region = models.ForeignKey(
        'Region',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Регион',
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
    capital = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Центр',
    )
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
    ls = models.LineStringField(blank=True, null=True, srid=4326, dim=3, verbose_name='Маршрут')
    ls2 = models.LineStringField(blank=True, null=True, srid=4326, dim=2, verbose_name='2D-маршрут')
    rt_length = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name='Длина',
    )
    rt_max_el = models.DecimalField(
        blank=True,
        null=True,
        max_digits=6,
        decimal_places=2,
        verbose_name='Максимальная высота',
    )
    rt_min_el = models.DecimalField(
        blank=True,
        null=True,
        max_digits=6,
        decimal_places=2,
        verbose_name='Минимальная высота',
    )
    rt_el_gain = models.DecimalField(
        blank=True,
        null=True,
        max_digits=7,
        decimal_places=2,
        verbose_name='Набор высоты',
    )
    rt_el_loss = models.DecimalField(
        blank=True,
        null=True,
        max_digits=7,
        decimal_places=2,
        verbose_name='Потеря высоты',
    )
    rt_type = models.CharField(
        max_length=1,
        choices=status,
        blank=True,
        default='h',
        verbose_name='Тип маршрута',
    )
    rt_is_gpx = models.BooleanField(default=False, verbose_name='GPX?')

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f'{self.rt_from} - {self.rt_to}'

    def save(self, *args, **kwargs):
        elevation_data = srtm.get_data()
        max_el, min_el, el_gain, el_loss, el, last_el = 0, 9999, 0, 0, 0, None
        coord_list = []

        for p in self.ls2.coords:
            # Добавляем высоту (нужно добавить проверку на её отсутсвие?)
            el = elevation_data.get_elevation(p[1], p[0])
            coord_list.append((p[0], p[1], el))

            # Максимальная/минимальная высота
            max_el = el if el > max_el else max_el
            min_el = el if el < min_el else min_el

            # Вычисляем набор/потерю высоты
            if last_el:
                if (el - last_el) > 0:
                    el_gain += (el - last_el)
                else:
                    el_loss -= (el - last_el)

            last_el = el

        ls = LineString(
            coord_list,
            srid=4326,
        )
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
