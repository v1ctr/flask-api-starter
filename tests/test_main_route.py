import unittest
from app import create_app, db


class MainRouteTestCase(unittest.TestCase):
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

    def test_public(self):
        # register a new account
        response = self.client.get('/public')
        self.assertEqual(response.status_code, 200)

    def test_private(self):
        # register a new account
        response = self.client.get('/private')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/auth/signup', json={
            "email": "test@gmail.com",
            "password": "12345"
        })
        self.assertEqual(response.status_code, 201)
        access_token = response.get_json().get('access_token')

        response = self.client.get('/private',
                                   headers={
                                       'Authorization': 'Bearer ' + access_token,
                                       'Accept': 'application/json',
                                       'Content-Type': 'application/json'
                                   })
        self.assertEqual(response.status_code, 200)



