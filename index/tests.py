from django.contrib.auth.models import User
from django.contrib.gis.geos import fromfile
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from findyourhappiness.settings import BASE_DIR

from faker import Faker

from index.models import City, Place, Route, Type

fake = Faker()

fake_placename = fake.name()

fake_name = fake.user_name()
fake_email = fake.email()
fake_pass = fake.password()


class SpecialUserPageReverseTestCase(TestCase):
    def setUp(self):
        User.objects.create(username=fake_name, email=fake_email)
        City.objects.create(title=fake_placename)
        type_place = Type.objects.create(title=fake_placename)
        self.place = Place.objects.create(title=fake_placename, is_published=True, type_place=type_place)

        self.c = Client()

    def test_mainpage_code(self):
        # Проверяем доступность главных страниц сайта
        self.assertEqual(self.c.get(reverse('index:index')).status_code, 200)
        self.assertEqual(self.c.get(reverse('index:indexlist')).status_code, 200)
        self.assertEqual(self.c.get(reverse('index:indexmap')).status_code, 200)

    def test_anon_placepage_code(self):
        # Проверяем доступность страниц мест анониму
        self.assertEqual(self.c.get(reverse('index:place', kwargs={'pk': self.place.id})).status_code, 200)
        self.assertEqual(self.c.get(reverse('index:place_edit', kwargs={'pk': self.place.id})).status_code, 302)
        self.assertEqual(self.c.get(reverse('index:place_create')).status_code, 302)
        self.assertEqual(self.c.get(reverse('index:route_edit', kwargs={'pk': self.place.id})).status_code, 302)
        self.assertEqual(self.c.get(reverse('index:route_create')).status_code, 302)
        self.assertEqual(self.c.get(reverse('index:route_create_pk', kwargs={'pk': self.place.id})).status_code, 302)

    def test_route_create(self):
        # Проверяем создание маршрутов
        ls = fromfile(BASE_DIR + '/test_fixtures/test.wkt')
        ls2 = fromfile(BASE_DIR + '/test_fixtures/test2.wkt')
        Route.objects.create(rt_title=fake_placename, rt_to=self.place, ls2=ls2)
        Route.objects.create(rt_title=fake_placename, rt_to=self.place, ls=ls)
