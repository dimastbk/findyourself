def pretty_coord(_lat, _lon):
    # принимает координаты и выводит в геоформате
    # fixme: не смотрит на знак, для Чукотки нужно будет поправить
    lat = f'{int(_lat)}° {int(_lat * 60 % 60)}\' {int(_lat * 3600 % 60)}\" в.д.'
    lon = f'{int(_lon)}° {int(_lon * 60 % 60)}\' {int(_lon * 3600 % 60)}\" с.ш.'
    return {'lat': lat, 'lon': lon}
