import unittest
import sys
import os
from flask_testing import TestCase
from server.models import User, Package
from server.forms import LoginForm, RegisterForm
from models import db, User, Package  

class TestMain(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for tests
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test Examples

    def test_index_route_requires_login(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login')  # Should redirect to login page

    def test_index_route_with_login(self):
        # Create a test user and log them in
        user = User(username='testuser', password='password')
        db.session.add(user)
        db.session.commit()

        with self.client.session_transaction() as session:
            session['user_id'] = user.id

        response = self.client.get('/')
        self.assert200(response) 



    # Add more tests for login, registration, tracking functionality, etc.
import pytest
from server import create_app, db
from server.models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_register(test_client):
    response = test_client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data

def test_login(test_client):
    test_client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = test_client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_logout(test_client):
    test_client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data
