from django.test import TestCase


class CategoryViews(TestCase):
    """
    A class for testing categories views
    """
    def test_get_categories_page(self):
        """
        This test checks if the exercise page is displayed
        """
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')
