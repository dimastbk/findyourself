from django.contrib.sites.shortcuts import get_current_site

import simplekml as mod_kml
from gpxpy import gpx as mod_gpx


def makeoncekml(route):
    kml = mod_kml.Kml(name=route.rt_title)
    kml.newpoint(name=route.rt_from.title, coords=route.rt_from.get_coord)
    kml.newpoint(name=route.rt_to.title, coords=route.rt_to.get_coord)
    kml.newlinestring(
        name=route.rt_title,
        description=tr_description(route),
        coords=route.get_coord,
    )
    return kml.kml()


def makeoncegpx(route):
    gpx = mod_gpx.GPX()

    gpx.waypoints.append(mod_gpx.GPXWaypoint(
        route.rt_from.coord.y,
        route.rt_from.coord.x,
        name=route.rt_from.title,
    ))
    gpx.waypoints.append(mod_gpx.GPXWaypoint(
        route.rt_to.coord.y,
        route.rt_to.coord.x,
        name=route.rt_to.title,
    ))

    gpx_route = mod_gpx.GPXRoute(
        name=route.rt_title,
        description=tr_description(route),
    )
    gpx.routes.append(gpx_route)

    for point in route.ls:
        gpx_route.points.append(mod_gpx.GPXRoutePoint(point[1], point[0]))

    return gpx.to_xml()


def makeallkml(routes):
    kml = mod_kml.Kml(name=routes.title)

    kml.newpoint(name=routes.title, coords=routes.get_coord)

    from_list = []
    for route in routes.route_place.all():
        if route.rt_from.title not in from_list:
            kml.newpoint(name=route.rt_from.title, coords=route.rt_from.get_coord)
            from_list.append(route.rt_from.title)
        kml.newlinestring(
            name=route.rt_title,
            description=tr_description(route),
            coords=route.get_coord,
        )

    return kml.kml()


def makeallgpx(routes):
    gpx = mod_gpx.GPX()

    gpx.waypoints.append(mod_gpx.GPXWaypoint(
        routes.coord.y,
        routes.coord.x,
        name=routes.title,
    ))

    from_list = []
    for route in routes.route_place.all():
        if route.rt_from.title not in from_list:
            gpx.waypoints.append(mod_gpx.GPXWaypoint(
                route.rt_from.coord.y,
                route.rt_from.coord.x,
                name=route.rt_from.title,
            ))
            from_list.append(route.rt_from.title)

        gpx_route = mod_gpx.GPXRoute(
            name=route.rt_title,
            description=tr_description(route),
        )
        gpx.routes.append(gpx_route)

        for point in route.ls:
            gpx_route.points.append(mod_gpx.GPXRoutePoint(point[1], point[0]))

    return gpx.to_xml()


def tr_description(rt):
    return (f"""<![CDATA[
        <b>Тип:</b> {rt.get_rt_type_display()}<br>
        <b>Начало:</b> {rt.rt_from}<br>
        <b>Конец:</b> {rt.rt_to}<br>
        <b>Длина:</b> {rt.rt_length} км<br>
        <div style="text-align: center; font-weight: bold;">
            <a href="http://{get_current_site(None).domain}">Взято отсюда</a>
        </div>
    ]]>""")
