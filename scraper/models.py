from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_scraped = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_scraped']