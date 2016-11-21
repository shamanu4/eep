from django.test import TestCase


class HomepageTestCase(TestCase):
    def test_login_page(self):
        """Visiting the application homepage should display a nice welcome message"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Програма Енергоеффективності міста Умань")
