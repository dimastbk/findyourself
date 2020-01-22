from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test.client import Client

from faker import Faker

from index.models import Place, Type

fake = Faker()


class UserProfileCreateTestCase(TestCase):

    fake_name = fake.user_name()
    fake_email = fake.email()
    fake_pass = fake.password()

    def setUp(self):
        user = User.objects.create(username=self.fake_name, email=self.fake_email)
        user.set_password(self.fake_pass)
        user.profile.instagram = 'test'
        user.save()

    def test_profile(self):
        # проверяем создание профиля
        user = User.objects.get(username=self.fake_name)
        self.assertEqual(user.id, user.profile.user.id)

    def test_ig_link(self):
        # добавление информации в профиль
        user = User.objects.get(username=self.fake_name)
        self.assertEqual(user.profile.get_ig_link(), 'https://www.instagram.com/test/')


class SpecialUserPageReverseTestCase(TestCase):

    fake_name = fake.user_name()
    fake_email = fake.email()
    fake_pass = fake.password()

    fake_name_2 = fake.user_name()
    fake_email_2 = fake.email()
    fake_pass_2 = fake.password()

    def setUp(self):
        user = User.objects.create(username=self.fake_name, email=self.fake_email)
        user.set_password(self.fake_pass)
        user.save()

    def test_anon_specialpage_code(self):
        c = Client()
        self.assertEqual(c.get(reverse('user:registration')).status_code, 200)
        self.assertEqual(c.get(reverse('user:login')).status_code, 200)
        self.assertEqual(c.get(reverse('user:logout')).status_code, 302)

    def test_anon_user_page(self):
        c = Client()
        user = User.objects.get(username=self.fake_name)
        self.assertEqual(
            c.get(
                reverse('user:current_user_favor_place', kwargs={'type_list': 'likes'}),
            ).status_code,
            302,
        )
        self.assertEqual(c.get(reverse('user:profile', kwargs={'pk': user.id})).status_code, 200)
        self.assertEqual(c.get(reverse('user:edit_profile')).status_code, 302)
        self.assertEqual(c.get(reverse('user:current_profile')).status_code, 302)
        self.assertEqual(c.get(reverse('user:password_change')).status_code, 302)

    def test_login_code(self):
        c = Client()
        self.assertEqual(
            c.post(reverse('user:login'), {'username': 'john', 'password': 'smith'}).status_code,
            200,
        )
        self.assertEqual(
            c.post(
                reverse('user:login'), {'username': self.fake_name, 'password': self.fake_pass},
            ).status_code,
            302,
        )

    def test_registration_page(self):
        c = Client()
        # Должно вернуть на страницу, так как пароль короткий
        self.assertEqual(
            c.post(
                reverse('user:registration'),
                {'username': 'john', 'password1': 'smith', 'password2': 'smith'},
            ).status_code,
            200,
        )
        # Должно вернуть на страницу, так как юзер существует
        self.assertEqual(
            c.post(
                reverse('user:registration'),
                {
                    'username': self.fake_name,
                    'password1': self.fake_pass,
                    'password2': self.fake_pass,
                },
            ).status_code,
            200,
        )

    def test_login_after_registration_code(self):
        # должны быть редиректы
        c = Client()
        self.assertRedirects(
            c.post(
                reverse('user:registration'),
                {
                    'username': self.fake_name_2,
                    'password1': self.fake_pass_2,
                    'password2': self.fake_pass_2,
                },
            ),
            reverse('user:edit_profile'),
        )
        self.assertRedirects(
            c.post(
                reverse('user:login'), {'username': self.fake_name_2, 'password': self.fake_pass_2},
            ),
            reverse('index'),
        )

    def test_login_user_page(self):
        c = Client()
        c.login(username=self.fake_name, password=self.fake_pass)
        user = User.objects.get(username=self.fake_name)
        self.assertEqual(
            c.get(
                reverse('user:current_user_favor_place', kwargs={'type_list': 'likes'}),
            ).status_code,
            200,
        )
        self.assertEqual(c.get(reverse('user:profile', kwargs={'pk': user.id})).status_code, 200)
        self.assertEqual(c.get(reverse('user:edit_profile')).status_code, 200)
        self.assertEqual(c.get(reverse('user:current_profile')).status_code, 200)
        self.assertEqual(c.get(reverse('user:password_change')).status_code, 200)


class UserLikesTestCase(TestCase):

    fake_name = fake.user_name()
    fake_email = fake.email()
    fake_pass = fake.password()

    fake_placename = fake.name()

    def setUp(self):
        user = User.objects.create(username=self.fake_name, email=self.fake_email)
        user.set_password(self.fake_pass)
        user.save()

        type_place = Type.objects.create(title='test')
        Place.objects.create(title=self.fake_placename, type_place=type_place, is_published=True)

    def test_likes_profile(self):
        c = Client()
        c.login(username=self.fake_name, password=self.fake_pass)
        user = User.objects.get(username=self.fake_name)
        place = Place.objects.get(title=self.fake_placename)
        self.assertRedirects(
            c.get(
                reverse('action_user_place', kwargs={'pk': place.id, 'action': 'like'}),
            ),
            reverse('place', kwargs={'pk': place.id}),
        )
        self.assertContains(
            c.get(
                reverse('place', kwargs={'pk': place.id}),
            ),
            self.fake_placename,
        )
