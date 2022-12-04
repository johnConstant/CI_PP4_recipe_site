from django.test import TestCase


class TestHomeViews(TestCase):
    """
    A class for testing homepage views
    """
    def test_get_home_page(self):
        """
        This test checks if the home page is displayed
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_search_page(self):
        """
        This test checks if the search results page is displayed
        """
        response = self.client.get('/search/?q=Recipe')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
