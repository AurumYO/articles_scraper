from ddf import G

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from scraper.views import HomeView
from scraper.views import ArticleListView
from scraper.views import RunScraperView
from scraper.models import Article


class HomeViewTest(TestCase):

    def setUp(self):
        self.user = G(get_user_model(), is_staff=False)
        self.staff_user = G(get_user_model(), is_staff=True)
        self.superuser = G(get_user_model(), is_staff=True, is_superuser=True)
        self.url = reverse("home")

    def test_non_staff_user_is_restricted_from_acessing_home_page(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_staff_user_is_redirected_to_home_page(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_superuser_is_redirected_to_home_page(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_it_uses_correct_template(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "home.html")

    def test_unauthenticated_user_redirected_to_login_page(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class ArticleListViewTest(TestCase):

    def setUp(self):
        self.user = G(get_user_model(), is_staff=False)
        self.staff_user = G(get_user_model(), is_staff=True)
        self.superuser = G(get_user_model(), is_staff=True, is_superuser=True)
        self.url = reverse("article-list")

    def test_non_staff_user_is_restricted_from_acessing_home_page(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_staff_user_is_redirected_to_home_page(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_superuser_is_redirected_to_home_page(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_it_uses_correct_template(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "scraper/article_list.html")

    def test_unauthenticated_user_redirected_to_login_page(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class RunScraperViewTest(TestCase):

    def setUp(self):
        self.user = G(get_user_model(), is_staff=False)
        self.staff_user = G(get_user_model(), is_staff=True)
        self.superuser = G(get_user_model(), is_staff=True, is_superuser=True)
        self.url = reverse("run-scraper")

    @patch("scraper.views.scrape_articles")
    def test_non_staff_user_is_restricted_from_acessing_home_page(
        self, mock_scrape_articles
    ):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    @patch("scraper.views.scrape_articles")
    def test_staff_user_is_redirected_to_home_page(self, mock_scrape_articles):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Scraping task has been scheduled.")

    @patch("scraper.views.scrape_articles")
    def test_superuser_is_redirected_to_home_page(self, mock_scrape_articles):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Scraping task has been scheduled.")

    @patch("scraper.views.scrape_articles")
    def test_task_triggered(self, mock_scrape_articles):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        mock_scrape_articles.assert_called_once()

    def test_unauthenticated_user_redirected_to_login_page(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
