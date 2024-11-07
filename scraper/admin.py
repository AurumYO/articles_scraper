from django.contrib import admin

from scraper.models import Article

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = (
        'title',
        'url',
        'date_scraped',
    )

    search_fields = (
        'name',
        'original_name',
        'created_by__email',
        'country',
        'location',
    )
    ordering = ('title',)


admin.site.register(Article, ArticleAdmin)
