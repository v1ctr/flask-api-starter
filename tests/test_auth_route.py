import unittest
from app import create_app, db


class AuthRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        # register a new account
        response = self.client.post('/auth/signup', json={
            "email": "test@gmail.com",
            "password": "12345"
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.get_json().get('access_token'))
        self.assertTrue(response.get_json().get('refresh_token'))

        # log in with the new account
        response = self.client.post('/auth/login', json={
            "email": "test@gmail.com",
            "password": "12345"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json().get('access_token'))
        self.assertTrue(response.get_json().get('refresh_token'))

        # log in with the wrong credentials
        response = self.client.post('/auth/login', json={
            "email": "wrong@gmail.com",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.get_json().get('code'))
        self.assertTrue(response.get_json().get('description'))
        self.assertTrue(response.get_json().get('name'))
        self.assertFalse(response.get_json().get('access_token'))
        self.assertFalse(response.get_json().get('refresh_token'))

        # log in with missing credentials
        response = self.client.post('/auth/login', json={
            "email": "wrong@gmail.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.get_json().get('code'))
        self.assertTrue(response.get_json().get('description'))
        self.assertTrue(response.get_json().get('name'))
        self.assertFalse(response.get_json().get('access_token'))
        self.assertFalse(response.get_json().get('refresh_token'))

    def test_refresh(self):
        response = self.client.post('/auth/signup', json={
            "email": "test@gmail.com",
            "password": "12345"
        })
        self.assertEqual(response.status_code, 201)
        access_token = response.get_json().get('access_token')
        refresh_token = response.get_json().get('refresh_token')
        self.assertTrue(access_token)
        self.assertTrue(refresh_token)

        # Refresh with GET method should fail
        response = self.client.get('/auth/refresh')
        self.assertEqual(response.status_code, 405)

        # Refresh without token
        response = self.client.post('/auth/refresh')
        self.assertEqual(response.status_code, 401)

        # Refresh with access_token
        response = self.client.post('/auth/refresh',
                                   headers={
                                       'Authorization': 'Bearer ' + access_token,
                                       'Accept': 'application/json',
                                       'Content-Type': 'application/json'
                                   })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json().get('description'), "Only refresh tokens are allowed")

        # Refresh with refresh_token
        response = self.client.post('/auth/refresh',
                                   headers={
                                       'Authorization': 'Bearer ' + refresh_token,
                                       'Accept': 'application/json',
                                       'Content-Type': 'application/json'
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json().get('access_token'))




