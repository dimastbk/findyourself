import json

from .utils import pretty_coord


class CoordMixin():
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
            return [(i[1], i[0]) for i in self.ls.coords]
        return ''

    @property
    def get_jsoncoord(self):
        # если одна точка, то выдаём только её, иначе список точек
        return json.dumps(self.get_rvcoord[0] if len(self.get_rvcoord) == 1 else self.get_rvcoord)

    def get_pretty_coord(self):
        # координаты с с.ш. и в.д.
        if self.coord:
            return pretty_coord(self.coord.x, self.coord.y)
