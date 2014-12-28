from django.contrib.auth import models
from bookservices.tests import base


class SessionTest(base.TestCase):
    def setUp(self):
        super(SessionTest, self).setUp()
        models.User.objects.create_user('nany', 'nany@localhost', 'pwd')

    def test_login_works(self):
        r = self.client.post('/api/session/login', data={'username': 'nany', 'password': 'pwd'})
        self.assertEqual(200, r.status_code)
        self.assertJsonEqual({'username': 'nany', 'id': self.var('uid')}, r.data['user'])
        self.assertEqual(self.var('uid').value, self.client.session['_auth_user_id'])
        r = self.client.get('/api/session/user')
        self.assertEqual(200, r.status_code)
        self.assertJsonEqual({'username': 'nany', 'id': self.var('uid')}, r.data['user'])

    def test_incorrect_login_returns_403(self):
        r = self.client.post('/api/session/login', data={'username': 'nany', 'password': 'wrongo!'})
        self.assertEqual(403, r.status_code)
        r = self.client.get('/api/session/user')
        self.assertEqual(403, r.status_code)

    def test_incorrect_login_does_not_clear_authentication(self):
        # This behavior is a bit janky, but it's the default behavior.
        self.client.login(username='nany', password='pwd')
        r = self.client.post('/api/session/login', {'username': 'nany', 'password': 'wrongo!'})
        self.assertEqual(403, r.status_code)
        r = self.client.get('/api/session/user')
        self.assertEqual(200, r.status_code)
        self.assertJsonEqual({'username': 'nany', 'id': self.var('uid')}, r.data['user'])
        self.assertEqual(self.var('uid').value, self.client.session['_auth_user_id'])

    def test_logout_works(self):
        self.client.login(username='nany', password='pwd')
        r = self.client.post('/api/session/logout', data={})
        self.assertEqual(204, r.status_code)
        r = self.client.get('/api/session/user')
        self.assertEqual(403, r.status_code)
