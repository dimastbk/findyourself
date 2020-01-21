import json


class CoordMixin:
    @property
    def get_coord(self):
        # прямые координаты, используются в KML
        if getattr(self, 'coord', False):
            return [(self.coord.x, self.coord.y)]
        elif getattr(self, 'ls', False):
            return [(i[0], i[1]) for i in self.ls.coords]
        return ''

    @property
    def get_rvcoord(self):
        # обратные координаты, используются в JS (leaflet)
        if getattr(self, 'coord', False):
            return [(self.coord.y, self.coord.x)]
        elif getattr(self, 'ls', False):
            return [(round(i[1], 5), round(i[0], 5)) for i in self.ls.coords]
        return ''

    @property
    def get_jsoncoord(self):
        # если одна точка, то выдаём только её, иначе список точек
        return json.dumps(self.get_rvcoord[0] if len(self.get_rvcoord) == 1 else self.get_rvcoord)

    def get_pretty_coord(self):
        # координаты с с.ш. и в.д.
        if self.coord:
            return self._pretty_coord(self.coord.x, self.coord.y)

    def _pretty_coord(self, _lat, _lon):
        # принимает координаты и выводит в геоформате
        # fixme: не смотрит на знак, для Чукотки нужно будет поправить
        lat = f'{int(_lat)}° {int(_lat * 60 % 60)}\' {int(_lat * 3600 % 60)}\" в.д.'
        lon = f'{int(_lon)}° {int(_lon * 60 % 60)}\' {int(_lon * 3600 % 60)}\" с.ш.'
        return {'lat': lat, 'lon': lon}


class CssClassFormMixin:
    # Добавляет специальный класс для полей, не прощедших валидацию
    # Добавляет botstrap form-control для всех виджетов

    invalid_css_class = 'is-invalid'
    default_css_class = 'form-control'
    additional_css_class = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field_attrs = field.widget.attrs
            field_attrs.update(
                {
                    'class': '{0} {1} {2}'.format(
                        field_attrs.get('class', ''),
                        self.default_css_class,
                        self.additional_css_class,
                    ),
                },
            )

    def is_valid(self):
        for f in self.errors:
            if f != '__all__':
                field_attrs = self.fields[f].widget.attrs
                field_attrs.update(
                    {
                        'class': '{0} {1}'.format(
                            field_attrs.get('class', ''), self.invalid_css_class,
                        ),
                    },
                )
        return super().is_valid()
