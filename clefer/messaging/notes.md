from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from accounts.models import User
from messaging.models import Message
import io
from django.utils import timezone
from messaging.serializers import MessageSerializer
from accounts.serializers import UserSerializer


sender = User(1, 'pekka', 'p@p.com', 'pw')
sender.save()
receiver = User(1, 'kalle', 'pk@p.com', 'pw')
msg = Message(1, 'Hello, world!', timezone.now(), sender.id, receiver.id, False)
msg.save()
ms = MessageSerializer(msg)
us = UserSerializer(sender)
ms.data
us.data

mc = JSONRenderer().render(ms.data)
s = io.BytesIO(mc)
data = JSONParser().parse(s)
data
ms = MessageSerializer(data=data)
ms.is_valid()
ms.validated_data
ms.save()


serializer = MessageSerializer(Message.objects.all(), many=True)
serializer.data