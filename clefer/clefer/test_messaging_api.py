from rest_framework.test import APITestCase
from rest_framework import status
import json
from messaging.models import Message
from accounts.models import User

class MessageAPITest(APITestCase):
    
    def setUp(self):
        user1 = User.objects.create(username="p@p.com", password="pw")
        user1.save()
        user2 = User.objects.create(username="k@k.com", password="pw")
        user2.save()
        self.client.force_authenticate(user1)
        Message.objects.create(message_text="Test message", sender=user1, receiver=user2)

    def test_should_get_all_messages(self):
        # When
        response = self.client.get('/api/v1/messages/')
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message_text'], 'Test message')

    def test_should_get_zero_messages_when_filter_string_does_not_match(self):
        # When
        response = self.client.get('/api/v1/messages/?', {'qstring':'badstring'})
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_should_get_one_messages_when_filter_string_matches(self):
        # When
        response = self.client.get('/api/v1/messages/?', {'qstring':'message'})
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message_text'], 'Test message')

    def test_should_get_zero_messages_when_checking_received_messages(self):
        # When
        response = self.client.get('/api/v1/messages/received/')
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_should_get_one_messages_when_checking_sent_messages(self):
        # When
        response = self.client.get('/api/v1/messages/sent/')
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message_text'], 'Test message')

    def test_should_get_zero_messages_when_checking_unread_messages(self):
        # When
        response = self.client.get('/api/v1/messages/unread/')
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_should_get_one_message_when_checking_unread_messages(self):
        # Given
        self.client.force_authenticate(User.objects.get(username="k@k.com"))
        # When
        response = self.client.get('/api/v1/messages/unread/')
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message_text'], 'Test message')

    def test_should_get_a_message(self):
        # When
        response = self.client.get('/api/v1/messages/1/')
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message_text'], 'Test message')

    def test_should_successfully_send_a_message_to_user2(self):
        # Given
        User.objects.create(username="r@r.com", password="pw")
        created_user = User.objects.get(username="r@r.com")
        created_user_id = created_user.id
        data = {"message_text": "Hello, world!", "receiver_id": created_user_id}
        json_data = json.dumps(data)
        # When
        response = self.client.post('/api/v1/messages/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)

    def test_should_receive_a_400_when_missing_message_text(self):
        # Given
        User.objects.create(username="r@r.com", password="pw")
        created_user = User.objects.get(username="r@r.com")
        created_user_id = created_user.id
        data = {"receiver_id": created_user_id}
        json_data = json.dumps(data)
        # When
        response = self.client.post('/api/v1/messages/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Message.objects.count(), 1)

    def test_should_receive_a_400_when_missing_receiver_id(self):
        # Given
        data = {"message_text": "Hello, world!"}
        json_data = json.dumps(data)
        # When
        response = self.client.post('/api/v1/messages/', json_data, content_type='application/json')
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Message.objects.count(), 1)


        