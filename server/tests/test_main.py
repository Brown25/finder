import unittest
import sys
import os

# Add the path to the 'server' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server')))

from flask_testing import TestCase

from server.__init__ import create_app
from server.models import User, Package
from server.forms import LoginForm, RegisterForm, CreateLabelForm

class TestMainRoutes(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username='testuser', password=hashed_password)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        with self.client:
            self.client.post('/login', data=dict(username='testuser', password='testpassword'))
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Package Tracking System', response.data)

    def test_login_route(self):
        response = self.client.post('/login', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Package Tracking System', response.data)

        response = self.client.post('/login', data=dict(username='wronguser', password='wrongpassword'), follow_redirects=True)
        self.assertIn(b'Incorrect username or password', response.data)

    def test_logout_route(self):
        with self.client:
            self.client.post('/login', data=dict(username='testuser', password='testpassword'))
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Package Tracking System', response.data)

    def test_register_route(self):
        with self.client:
            response = self.client.post('/register', data=dict(username='newuser', password='newpassword', confirm_password='newpassword'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account created successfully!', response.data)

            response = self.client.post('/register', data=dict(username='testuser', password='testpassword', confirm_password='testpassword'), follow_redirects=True)
            self.assertIn(b'Username already exists', response.data)

    def test_create_label_route(self):
        with self.client:
            self.client.post('/login', data=dict(username='testuser', password='testpassword'))
            response = self.client.post('/create_label', data=dict(sender='Sender', recipient='Recipient', address='123 Test St'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Label created successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
