from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from faker import Faker

from index.models import City, Place, Type

fake = Faker()

fake_name = fake.user_name()
fake_email = fake.email()
fake_pass = fake.password()

fake_name_2 = fake.user_name()
fake_email_2 = fake.email()
fake_pass_2 = fake.password()

fake_placename = fake.name()


class UserProfileCreateTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=fake_name, email=fake_email)
        user.set_password(fake_pass)
        user.profile.instagram = fake_name
        user.save()

    def test_profile(self):
        # проверяем создание профиля
        user = User.objects.get(username=fake_name)
        self.assertEqual(user.id, user.profile.user.id)

    def test_ig_link(self):
        # добавление информации в профиль
        user = User.objects.get(username=fake_name)
        self.assertEqual(user.profile.get_ig_link(), f'https://www.instagram.com/{fake_name}/')


class SpecialUserPageReverseTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=fake_name, email=fake_email)
        user.set_password(fake_pass)
        user.save()

        City.objects.create(title=fake_placename)

        self.c = Client()

    def test_anon_specialpage_code(self):
        # Проверяем доступность страниц входа для анонов
        self.assertEqual(self.c.get(reverse('user:registration')).status_code, 200)
        self.assertEqual(self.c.get(reverse('user:login')).status_code, 200)
        self.assertEqual(self.c.get(reverse('user:logout')).status_code, 302)

    def test_anon_user_page(self):
        # Проверяем редиректы для анонов
        user = User.objects.get(username=fake_name)
        self.assertEqual(
            self.c.get(
                reverse('user:current_user_favor_place', kwargs={'type_list': 'likes'}),
            ).status_code,
            302,
        )
        self.assertEqual(
            self.c.get(reverse('user:profile', kwargs={'pk': user.id})).status_code, 200,
        )
        self.assertEqual(self.c.get(reverse('user:edit_profile')).status_code, 302)
        self.assertEqual(self.c.get(reverse('user:current_profile')).status_code, 302)
        self.assertEqual(self.c.get(reverse('user:password_change')).status_code, 302)

    def test_login_code(self):
        # Проверяем вход с левыми данными и существующими
        self.assertEqual(
            self.c.post(
                reverse('user:login'), {'username': 'john', 'password': 'smith'},
            ).status_code,
            200,
        )
        self.assertEqual(
            self.c.post(
                reverse('user:login'), {'username': fake_name, 'password': fake_pass},
            ).status_code,
            302,
        )

    def test_registration_page(self):
        # Должно вернуть на страницу, так как пароль короткий
        self.assertEqual(
            self.c.post(
                reverse('user:registration'),
                {'username': 'john', 'password1': 'smith', 'password2': 'smith'},
            ).status_code,
            200,
        )
        # Должно вернуть на страницу, так как юзер существует
        self.assertEqual(
            self.c.post(
                reverse('user:registration'),
                {'username': fake_name, 'password1': fake_pass, 'password2': fake_pass},
            ).status_code,
            200,
        )

    def test_login_after_registration_code(self):
        # должны быть редиректы
        self.assertRedirects(
            self.c.post(
                reverse('user:registration'),
                {'username': fake_name_2, 'password1': fake_pass_2, 'password2': fake_pass_2},
            ),
            reverse('user:edit_profile'),
        )
        self.assertRedirects(
            self.c.post(reverse('user:login'), {'username': fake_name_2, 'password': fake_pass_2}),
            reverse('index:index'),
        )

    def test_login_user_page(self):
        # проверяем доступность страниц после логина
        self.c.login(username=fake_name, password=fake_pass)
        user = User.objects.get(username=fake_name)
        self.assertEqual(
            self.c.get(
                reverse('user:current_user_favor_place', kwargs={'type_list': 'likes'}),
            ).status_code,
            200,
        )
        self.assertEqual(
            self.c.get(reverse('user:profile', kwargs={'pk': user.id})).status_code, 200,
        )
        self.assertEqual(self.c.get(reverse('user:edit_profile')).status_code, 200)
        self.assertEqual(self.c.get(reverse('user:current_profile')).status_code, 200)
        self.assertEqual(self.c.get(reverse('user:password_change')).status_code, 200)

    def test_edit_user_page(self):
        # Проверяем редактирование пользователя
        self.c.login(username=fake_name, password=fake_pass)
        user = User.objects.get(username=fake_name)
        city = City.objects.get(title=fake_placename)
        self.assertRedirects(
            self.c.post(
                reverse('user:edit_profile'),
                {'username': f'{fake_name}@{fake_name}', 'city': city.id},
            ),
            reverse('user:current_profile'),
        )
        self.assertContains(
            self.c.get(reverse('user:profile', kwargs={'pk': user.id})), f'{fake_name}@{fake_name}',
        )


class UserLikesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=fake_name, email=fake_email)
        user.set_password(fake_pass)
        user.save()

        type_place = Type.objects.create(title='test')
        Place.objects.create(title=fake_placename, type_place=type_place, is_published=True)

        self.c = Client()

    def test_likes_profile(self):
        # Проверяем возможность ставить лайк, появление в списке и обратно
        self.c.login(username=fake_name, password=fake_pass)
        user = User.objects.get(username=fake_name)
        place = Place.objects.get(title=fake_placename)
        self.assertRedirects(
            self.c.get(reverse('user:action_user_place', kwargs={'pk': place.id, 'action': 'like'})),
            reverse('index:place', kwargs={'pk': place.id}),
        )
        self.assertContains(
            self.c.get(
                reverse('user:user_favor_place', kwargs={'pk': user.id, 'type_list': 'likes'}),
            ),
            fake_placename,
        )
        self.assertRedirects(
            self.c.get(reverse('user:action_user_place', kwargs={'pk': place.id, 'action': 'unlike'})),
            reverse('index:place', kwargs={'pk': place.id}),
        )
        self.assertNotContains(
            self.c.get(
                reverse('user:user_favor_place', kwargs={'pk': user.id, 'type_list': 'likes'}),
            ),
            fake_placename,
        )
