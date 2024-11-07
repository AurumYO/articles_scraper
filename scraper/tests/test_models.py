from ddf import G
from django.test import TestCase

from scraper.models import Article


class ArticleTest(TestCase):
    """
    Test case for the Article model's methods.

    """

    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.article = G(Article, title="Rose Rosalind")

    def test_it_has_string_representation(self):
        # test __str__ method for Band model
        self.assertEqual(str(self.article), "Rose Rosalind")
