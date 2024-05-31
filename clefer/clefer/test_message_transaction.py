from django.test import TransactionTestCase
import json
from messaging.models import Message
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class MessagingAPITestCase(TransactionTestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="k3@k.com", password="pw")
        self.user1.save()

    def test_post_message_should_receive_a_404_when_receiver_id_does_not_exist(self):
        # Given
        data = {"message_text": "Hello, world!", "receiver_id": 123}
        json_data = json.dumps(data)
        refresh = RefreshToken.for_user(self.user1)
        token = str(refresh.access_token)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        # When
        response = self.client.post('/api/v1/messages/', json_data, content_type='application/json', **headers)
        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(response.data, {'message': 'No receiver with that id found.'})
