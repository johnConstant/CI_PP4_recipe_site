from django.test import TestCase


class TestContactViews(TestCase):
    """
    A class for testing exercises views
    """
    def test_get_contact_page(self):
        """
        This test checks if the contact page is displayed
        """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
