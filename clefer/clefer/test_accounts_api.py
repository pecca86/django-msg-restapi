from django.test import TransactionTestCase
import json
from messaging.models import Message
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

class MessagingAPITestCase(TransactionTestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="k3@k.com", password="pw")
        self.user1.save()


    def test_should_login_user_and_return_tokens(self):
        # Given
        login_data = {"username": "k3@k.com", "password": "pw"}
        json_data = json.dumps(login_data)
        # When
        response = self.client.post('/api/v1/login/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(response.data['refresh'])

    def test_should_return_401_when_login_fails_for_non_existent_username(self):
        # Given
        login_data = {"username": "not@me.com", "password": "pw"}
        json_data = json.dumps(login_data)
        # When
        response = self.client.post('/api/v1/login/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, 401)

    def test_should_return_401_when_login_fails_for_wrong_password(self):
        # Given
        login_data = {"username": "k3@k.com", "password": "wrongpw"}
        json_data = json.dumps(login_data)
        # When
        response = self.client.post('/api/v1/login/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, 401)

    def test_should_register_user(self):
        # Given
        register_data = {"username": "test@t.com", "password": "pwpwpwpw"}
        json_data = json.dumps(register_data)
        # When
        response = self.client.post('/api/v1/users/create/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(User.objects.filter(username='test@t.com'))

    def test_should_return_400_when_username_not_valid_email_format(self):
        # Given
        register_data = {"username": "test", "password": "pwpwpwpw"}
        json_data = json.dumps(register_data)
        # When
        response = self.client.post('/api/v1/users/create/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, 400)

    def test_should_return_400_when_password_under_8_chars_long(self):
        # Given
        register_data = {"username": "test@tester.com", "password": "pwpw"}
        json_data = json.dumps(register_data)
        # When
        response = self.client.post('/api/v1/users/create/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, 400)

    def test_should_return_all_registered_users(self):
        refresh = RefreshToken.for_user(self.user1)
        token = str(refresh.access_token)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        user_id = self.user1.id
        # When
        response = self.client.get('/api/v1/users/', **headers)
        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'count': 1, 'next': None, 'previous': None, 'results': [{'id': user_id, 'username': 'k3@k.com'}]})

    def test_should_return_user_by_id_when_exists(self):
        refresh = RefreshToken.for_user(self.user1)
        token = str(refresh.access_token)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        user_id = self.user1.id
        # When
        response = self.client.get(f'/api/v1/users/{user_id}/', **headers)
        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': user_id, 'username': 'k3@k.com'})

    def test_should_return_404_when_user_not_found(self):
        refresh = RefreshToken.for_user(self.user1)
        token = str(refresh.access_token)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        user_id = 100
        # When
        response = self.client.get(f'/api/v1/users/{user_id}/', **headers)
        # Then
        self.assertEqual(response.status_code, 404)