import srtm
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
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
    )
    rt_to = models.ForeignKey(
        'Place',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Конечный пункт',
    )
    ls = models.LineStringField(blank=True, null=True, srid=4326, verbose_name='Маршрут')
    rt_length = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name='Длина',
    )
    rt_type = models.CharField(
        max_length=1,
        choices=status,
        blank=True,
        default='h',
        verbose_name='Тип маршрута',
    )

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f'{self.rt_from} - {self.rt_to}'

    def save(self, *args, **kwargs):
        # Добавляем высоту (нужно добавить проверку на её отсутсвие)
        elevation_data = srtm.get_data()
        ls = LineString(
            [(p[0], p[1], elevation_data.get_elevation(p[1], p[0])) for p in self.ls.coords],
            srid=4326,
        )
        # считаем зону UTM для корректного расчёта длины
        # ls.centroid.x - долгота центра маршрута
        zone = 32660 - round((177 - ls.centroid.x) / 6)
        ls.transform(zone)
        # Считаем длину маршрута
        self.rt_length = ls.length / 1000

        super().save(*args, **kwargs)
