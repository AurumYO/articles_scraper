from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("articles/", views.ArticleListView.as_view(), name="article-list"),
    path("run-scraper/", views.RunScraperView.as_view(), name="run-scraper"),
]
