from django.test import TestCase


class TestArticlesViews(TestCase):
    """
    A class for testing articles views
    """
    def test_get_articles_page(self):
        """
        This test checks if the articles page is displayed
        """
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles.html')
