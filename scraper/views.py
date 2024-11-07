from django.views.generic import ListView

from scraper.models import Article


class HomeView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 50


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 50