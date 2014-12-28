import unittest

from django.test import Client, TestCase
from django.contrib.auth.models import User


class ViewTest(TestCase):
    def setUp(self):
        super(ViewTest, self).setUp()
        self.client = Client()
        User.objects.create_user('nany', 'nany@localhost', 'pwd')

    def assertContextUserIsLoggedIn(self, response):
        self.assertTrue(response.context['user'].is_authenticated())

    def assertContextUserIsLoggedOut(self, response):
        self.assertFalse(response.context['user'].is_authenticated())

    def test_login_get_renders_form(self):
        r = self.client.get('/old/login')
        self.assertEqual(200, r.status_code)
        self.assertTemplateUsed(r, 'bookfront/login.html')

    def test_incorrect_login_renders_form(self):
        r = self.client.post('/old/login', {'username': 'nany', 'password': 'wrongo!'})
        self.assertContains(r, 'alert-error', status_code=200)
        self.assertTemplateUsed(r, 'bookfront/login.html')

    def test_incorrect_login_does_not_clear_authentication(self):
        # This behavior is a bit janky, but it's the default behavior.
        self.client.login(username='nany', password='pwd')
        r = self.client.post('/old/login', {'username': 'nany', 'password': 'wrongo!'})
        self.assertContains(r, 'alert-error', status_code=200)
        self.assertContextUserIsLoggedIn(r)

    @unittest.skip('to be removed')
    def test_correct_login_redirects_to_index_by_default(self):
        r = self.client.post('/old/login', {'username': 'nany', 'password': 'pwd'}, follow=True)
        self.assertEqual(200, r.status_code)
        self.assertTemplateUsed(r, 'bookfront/index.html')
        self.assertContextUserIsLoggedIn(r)

    def test_logout_works(self):
        self.client.login(username='nany', password='pwd')
        r = self.client.get('/old/logout')
        self.assertEqual(200, r.status_code)
        self.assertTemplateUsed(r, 'bookfront/logout.html')
        self.assertContextUserIsLoggedOut(r)
