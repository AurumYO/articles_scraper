from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView

from .utils import scrape_articles

from scraper.models import Article


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "home.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class ArticleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"
    paginate_by = 50

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class RunScraperView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        scrape_articles()  # Trigger the scraping task
        return HttpResponse("Scraping task has been scheduled.")
