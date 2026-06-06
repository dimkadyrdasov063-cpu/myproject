from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Category


class SignUpTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_page_loads(self):
        """Страница регистрации открывается"""
        response = self.client.get(reverse('articles:signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_creates_user(self):
        """Регистрация создаёт пользователя"""
        response = self.client.post(reverse('articles:signup'), {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_redirects_after_success(self):
        """После регистрации редиректит на список статей"""
        response = self.client.post(reverse('articles:signup'), {
            'username': 'testuser2',
            'email': 'test2@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('articles:article_list'))

    def test_signup_wrong_passwords(self):
        """Регистрация с разными паролями не работает"""
        response = self.client.post(reverse('articles:signup'), {
            'username': 'testuser3',
            'email': 'test3@test.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass123!',
        })
        self.assertFalse(User.objects.filter(username='testuser3').exists())


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!'
        )

    def test_login_page_loads(self):
        """Страница входа открывается"""
        response = self.client.get(reverse('articles:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_works(self):
        """Вход с правильными данными работает"""
        response = self.client.post(reverse('articles:login'), {
            'username': 'testuser',
            'password': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        """Вход с неправильным паролем не работает"""
        response = self.client.post(reverse('articles:login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)


class ArticleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!'
        )
        self.article = Article.objects.create(
            title='Тестовая статья',
            content='Контент статьи',
            author=self.user,
            is_published=True,
        )

    def test_article_list_loads(self):
        """Список статей открывается"""
        response = self.client.get(reverse('articles:article_list'))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_loads(self):
        """Страница статьи открывается"""
        response = self.client.get(reverse('articles:article_detail', args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_404(self):
        """Несуществующая статья возвращает 404"""
        response = self.client.get(reverse('articles:article_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_article_views_count(self):
        """Просмотры статьи увеличиваются"""
        views_before = self.article.views_count
        self.client.get(reverse('articles:article_detail', args=[self.article.pk]))
        self.article.refresh_from_db()
        self.assertEqual(self.article.views_count, views_before + 1)

    def test_create_article_requires_login(self):
        """Создание статьи без авторизации редиректит на логин"""
        response = self.client.get(reverse('articles:create_article'))
        self.assertEqual(response.status_code, 302)

    def test_create_article_logged_in(self):
        """Авторизованный пользователь может создать статью"""
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.post(reverse('articles:create_article'), {
            'title': 'Новая статья',
            'content': 'Контент',
            'is_published': True,
        })
        self.assertTrue(Article.objects.filter(title='Новая статья').exists())

    def test_search_works(self):
        """Поиск находит статью по названию"""
        response = self.client.get(reverse('articles:article_list') + '?q=Тестовая')
        self.assertContains(response, 'Тестовая статья')

    def test_search_no_results(self):
        """Поиск по несуществующему слову не ломается"""
        response = self.client.get(reverse('articles:article_list') + '?q=блабла123')
        self.assertEqual(response.status_code, 200)

    def test_edit_article_only_author(self):
        """Чужую статью редактировать нельзя"""
        other_user = User.objects.create_user(username='other', password='StrongPass123!')
        self.client.login(username='other', password='StrongPass123!')
        response = self.client.get(reverse('articles:article_edit', args=[self.article.pk]))
        self.assertEqual(response.status_code, 404)

    def test_delete_article_only_author(self):
        """Чужую статью удалить нельзя"""
        other_user = User.objects.create_user(username='other2', password='StrongPass123!')
        self.client.login(username='other2', password='StrongPass123!')
        response = self.client.post(reverse('articles:article_delete', args=[self.article.pk]))
        self.assertTrue(Article.objects.filter(pk=self.article.pk).exists())


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!'
        )

    def test_profile_requires_login(self):
        """Профиль без авторизации редиректит"""
        response = self.client.get(reverse('articles:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_loads_when_logged_in(self):
        """Профиль открывается для авторизованного"""
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(reverse('articles:profile'))
        self.assertEqual(response.status_code, 200)

    def test_my_articles_loads(self):
        """Мои статьи открываются"""
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(reverse('articles:my_articles'))
        self.assertEqual(response.status_code, 200)
