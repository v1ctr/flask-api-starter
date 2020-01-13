import unittest
from app import create_app, db, mail


class MailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_send_mail(self):
        with mail.record_messages() as outbox:
            mail.send_message(subject='testing',
                              body='test',
                              recipients=['test@example.com'])

            assert len(outbox) == 1
            assert outbox[0].subject == "testing"

